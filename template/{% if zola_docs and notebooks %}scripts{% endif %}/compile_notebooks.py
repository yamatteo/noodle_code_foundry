#!/usr/bin/env python3
"""
Notebook Compilation Script

This script compiles Jupyter notebooks from ./notebooks to ./zdocs/content/compiled_notebooks
as markdown with proper Zola TOML front matter.

Features:
- Sequential execution to avoid resource exhaustion
- Progress indication and timing
- Graceful error handling
- Automatic Zola front matter injection
- Proper image path handling
"""

import os
import sys
import time
import traceback
from pathlib import Path
from datetime import datetime
import papermill as pm
import nbconvert
import nbformat
from nbconvert import MarkdownExporter
import json
import re
import argparse

# Configuration
NOTEBOOKS_DIR = Path("notebooks")
OUTPUT_DIR = Path("zdocs/content/compiled_notebooks")
STATIC_DIR = Path("zdocs/static/compiled_notebooks")
PROCESSED_DIR = Path("/tmp/processed_notebooks")

# Zola front matter template
ZOLA_FRONT_MATTER_TEMPLATE = """+++
title = "{title}"
description = "{description}"
weight = {weight}
draft = false
template = "page.html"
in_search_index = true

[extra]
notebook_source = "{notebook_source}"
generated_date = "{generated_date}"
execution_time = "{execution_time}"
cell_count = {cell_count}
+++

"""

def setup_directories():
    """Create necessary directories if they don't exist."""
    NOTEBOOKS_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)

def extract_notebook_metadata(notebook_path):
    """Extract metadata from notebook for front matter generation."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Extract title from first markdown cell
        title = "Untitled Notebook"
        description = "Generated from Jupyter notebook"
        tags = ["jupyter", "python"]
        
        for cell in notebook.cells:
            if cell.cell_type == "markdown" and cell.source:
                # Try to extract title from first markdown cell
                lines = cell.source.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break
                    elif line and not line.startswith('#') and len(line) > 10:
                        description = line[:100] + "..." if len(line) > 100 else line
                break
        
        # Infer tags from notebook filename and content
        filename = notebook_path.stem.lower()
        if "math" in filename or "calculus" in filename:
            tags.extend(["mathematics", "calculus"])
        if "data" in filename or "visualization" in filename:
            tags.extend(["data-science", "visualization"])
        if "statistical" in filename or "analysis" in filename:
            tags.extend(["statistics", "analysis"])
        if "ml" in filename or "machine" in filename:
            tags.extend(["machine-learning"])
        
        # Count cells
        cell_count = len(notebook.cells)
        
        return {
            'title': title,
            'description': description,
            'tags': json.dumps(tags),
            'cell_count': cell_count,
            'notebook_source': notebook_path.name
        }
    
    except Exception as e:
        print(f"Warning: Could not extract metadata from {notebook_path}: {e}")
        return {
            'title': notebook_path.stem.replace('_', ' ').title(),
            'description': "Generated from Jupyter notebook",
            'tags': json.dumps(["jupyter", "python"]),
            'cell_count': 0,
            'notebook_source': notebook_path.name
        }

def execute_notebook(notebook_path, output_path):
    """Execute a notebook using Papermill."""
    try:
        print(f"  Executing notebook...")
        start_time = time.time()
        
        # Execute notebook with Papermill
        pm.execute_notebook(
            input_path=notebook_path,
            output_path=output_path,
            kernel_name='python3',
            progress_bar=False
        )
        
        execution_time = time.time() - start_time
        print(f"  ✓ Execution completed in {execution_time:.2f} seconds")
        return execution_time, None
        
    except Exception as e:
        error_msg = f"Execution failed: {str(e)}"
        print(f"  ✗ {error_msg}")
        return 0, error_msg

def convert_to_markdown(notebook_path, output_dir):
    """Convert executed notebook to markdown."""
    try:
        print(f"  Converting to markdown...")
        
        # Create Markdown exporter
        exporter = MarkdownExporter()
        
        # Read the executed notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Convert to markdown
        (body, resources) = exporter.from_notebook_node(notebook)
        
        return body, resources, None
        
    except Exception as e:
        error_msg = f"Conversion failed: {str(e)}"
        print(f"  ✗ {error_msg}")
        return None, None, error_msg

def inject_zola_front_markdown(markdown_content, metadata, execution_time):
    """Inject Zola front matter into markdown content."""
    try:
        # Prepare front matter
        front_matter = ZOLA_FRONT_MATTER_TEMPLATE.format(
            title=metadata['title'],
            description=metadata['description'],
            date=datetime.now().strftime('%Y-%m-%d'),
            weight=0,  # Can be customized later
            tags=metadata['tags'],
            notebook_source=metadata['notebook_source'],
            generated_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            execution_time=f"{execution_time:.2f}s",
            cell_count=metadata['cell_count']
        )
        
        # Combine front matter with content
        final_content = front_matter + markdown_content
        
        return final_content, None
        
    except Exception as e:
        error_msg = f"Front matter injection failed: {str(e)}"
        return None, error_msg

def fix_image_paths(markdown_content, notebook_name):
    """Fix image paths in markdown content for Zola."""
    try:
        # Pattern to match markdown image links
        # ![alt](path/to/image.png)
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        
        # Convert underscores to dashes to match Zola's slugification
        zola_dir_name = notebook_name.replace('_', '-')
        
        def replace_image_path(match):
            alt_text = match.group(1)
            original_path = match.group(2)
            
            # If it's a relative path from nbconvert, adjust it
            if original_path.startswith('./'):
                # Remove ./ - use relative path since we're in the same directory
                filename = original_path[2:]
                new_path = filename
            elif original_path.startswith('../'):
                # Handle relative paths
                new_path = original_path
            else:
                # Use relative path since we're in the same directory
                new_path = original_path
            
            return f'![{alt_text}]({new_path})'
        
        # Apply the replacement
        fixed_content = re.sub(image_pattern, replace_image_path, markdown_content)
        
        return fixed_content, None
        
    except Exception as e:
        error_msg = f"Image path fixing failed: {str(e)}"
        return None, error_msg

def copy_assets(resources, notebook_name, output_dir):
    """Copy assets (images, etc.) to the static directory."""
    try:
        if 'outputs' in resources and resources['outputs']:
            # Convert underscores to dashes to match Zola's slugification
            zola_dir_name = notebook_name.replace('_', '-')
            notebook_dir = STATIC_DIR / zola_dir_name
            notebook_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in resources['outputs'].items():
                # Create output file path in static directory
                output_file = notebook_dir / filename
                
                # Create parent directories if needed
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Write the file
                with open(output_file, 'wb') as f:
                    f.write(content)
                
                print(f"  ✓ Copied asset: static/compiled_notebooks/{zola_dir_name}/{filename}")
        
        return None
        
    except Exception as e:
        error_msg = f"Asset copying failed: {str(e)}"
        return error_msg

def process_notebook(notebook_path, output_dir):
    """Process a single notebook: execute, convert, and add front matter."""
    notebook_name = notebook_path.stem
    print(f"\n📓 Processing: {notebook_name}")
    print("=" * 50)
    
    # Step 1: Extract metadata
    print("📋 Extracting metadata...")
    metadata = extract_notebook_metadata(notebook_path)
    print(f"  Title: {metadata['title']}")
    print(f"  Tags: {metadata['tags']}")
    
    # Step 2: Execute notebook
    print("⚡ Executing notebook...")
    executed_notebook_path = PROCESSED_DIR / f"{notebook_name}_executed.ipynb"
    execution_time, execution_error = execute_notebook(notebook_path, executed_notebook_path)
    
    if execution_error:
        return False, execution_error
    
    # Step 3: Convert to markdown
    print("🔄 Converting to markdown...")
    markdown_content, resources, conversion_error = convert_to_markdown(executed_notebook_path, output_dir)
    
    if conversion_error:
        return False, conversion_error
    
    # Step 4: Fix image paths
    print("🖼️  Fixing image paths...")
    fixed_content, path_error = fix_image_paths(markdown_content, notebook_name)
    
    if path_error:
        return False, path_error
    
    # Step 5: Inject Zola front matter
    print("📝 Injecting Zola front matter...")
    final_content, front_matter_error = inject_zola_front_markdown(fixed_content, metadata, execution_time)
    
    if front_matter_error:
        return False, front_matter_error
    
    # Step 6: Write final markdown file
    output_file = output_dir / f"{notebook_name}.md"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"  ✓ Markdown saved: {output_file}")
    except Exception as e:
        return False, f"Failed to write markdown file: {str(e)}"
    
    # Step 7: Copy assets
    print("📁 Copying assets...")
    asset_error = copy_assets(resources, notebook_name, output_dir)
    
    if asset_error:
        return False, asset_error
    
    # Clean up executed notebook
    try:
        executed_notebook_path.unlink()
    except:
        pass
    
    print(f"✅ Successfully processed: {notebook_name}")
    return True, None

def generate_section_index(output_dir):
    """Generate _index.md for the compiled_notebooks section."""
    try:
        index_content = """+++
title = "Compiled Notebooks"
description = "Jupyter notebooks compiled to static documentation"
sort_by = "weight"
weight = 0
template = "section.html"
in_search_index = true

[extra]
section_type = "notebooks"
generated_date = "{}"
+++

# Compiled Notebooks

This section contains Jupyter notebooks that have been compiled to static documentation format.

## Available Notebooks

""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # List all markdown files (excluding _index.md)
        md_files = sorted([f for f in output_dir.glob("*.md") if f.name != "_index.md"])
        
        for md_file in md_files:
            # Read the front matter to get title
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from front matter
            title = md_file.stem.replace('_', ' ').title()
            for line in content.split('\n'):
                if line.startswith('title = '):
                    title = line.split(' = ')[1].strip('"')
                    break
            
            # Convert filename to Zola URL format (underscores to dashes)
            url_name = md_file.stem.replace('_', '-')
            index_content += f"- [{title}]({url_name}/)\n"
        
        # Write the index file
        index_file = output_dir / "_index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"  ✓ Generated section index: {index_file}")
        return None
        
    except Exception as e:
        error_msg = f"Section index generation failed: {str(e)}"
        return error_msg

def main():
    """Main compilation function."""
    parser = argparse.ArgumentParser(description="Compile Jupyter notebooks for Zola")
    parser.add_argument("--notebook", nargs="?", help="Specific notebook to process (optional)")
    parser.add_argument("--clean", action="store_true", help="Clean output directory before processing")
    args = parser.parse_args()
    
    print("🚀 Starting Notebook Compilation")
    print("=" * 50)
    
    # Setup directories
    setup_directories()
    
    # Clean output directory if requested
    if args.clean:
        print("🧹 Cleaning output directory...")
        for file in OUTPUT_DIR.glob("*.md"):
            file.unlink()
        for asset_dir in OUTPUT_DIR.iterdir():
            if asset_dir.is_dir():
                import shutil
                shutil.rmtree(asset_dir)
        
        # Also clean static directory
        if STATIC_DIR.exists():
            print("  🧹 Cleaning static compiled_notebooks directory...")
            import shutil
            shutil.rmtree(STATIC_DIR)
        
        print("  ✓ Output and static directories cleaned")
    
    # Find notebooks to process
    if args.notebook:
        notebook_files = [NOTEBOOKS_DIR / args.notebook]
        if not notebook_files[0].exists():
            print(f"❌ Notebook not found: {args.notebook}")
            sys.exit(1)
    else:
        notebook_files = list(NOTEBOOKS_DIR.glob("*.ipynb"))
        if not notebook_files:
            print("❌ No notebooks found in ./notebooks directory")
            sys.exit(1)
    
    print(f"📚 Found {len(notebook_files)} notebook(s) to process")
    
    # Process notebooks
    successful = []
    failed = []
    total_start_time = time.time()
    
    for notebook_path in notebook_files:
        success, error = process_notebook(notebook_path, OUTPUT_DIR)
        
        if success:
            successful.append(notebook_path.name)
        else:
            failed.append((notebook_path.name, error))
    
    # Summary
    total_time = time.time() - total_start_time
    print("\n" + "=" * 50)
    print("📊 COMPILATION SUMMARY")
    print("=" * 50)
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Successfully processed: {len(successful)}/{len(notebook_files)}")
    
    if successful:
        print(f"\n✅ Successful:")
        for notebook in successful:
            print(f"  - {notebook}")
    
    if failed:
        print(f"\n❌ Failed:")
        for notebook, error in failed:
            print(f"  - {notebook}: {error}")
    
    # Final message
    if successful:
        # Generate section index
        print("\n📋 Generating section index...")
        index_error = generate_section_index(OUTPUT_DIR)
        if index_error:
            print(f"  ⚠️  Warning: {index_error}")
        
        print(f"\n🎉 Compilation completed!")
        print(f"📂 Output directory: {OUTPUT_DIR}")
        print(f"📖 Ready for Zola build: zola build")
    else:
        print(f"\n💥 Compilation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
