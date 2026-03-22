# Jupyter Notebooks

This directory contains Jupyter notebooks that demonstrate various data science, mathematical, and visualization concepts. These notebooks are compiled into markdown files for inclusion in the Zola documentation site.

## Available Notebooks

### 1. mathematical_concepts.ipynb
**Topics**: Calculus, Linear Algebra, Probability, Fourier Analysis

This notebook demonstrates fundamental mathematical concepts with visualizations:
- **Calculus**: Derivatives and integrals with function visualization
- **Linear Algebra**: Eigenvalues and eigenvectors with geometric interpretations
- **Probability Theory**: Normal distributions and the Central Limit Theorem
- **Fourier Analysis**: Signal decomposition and frequency analysis

**Key Features**:
- Extensive LaTeX mathematical notation
- Interactive matplotlib visualizations
- Statistical demonstrations with scipy
- Mathematical proofs and explanations

### 2. data_visualization.ipynb
**Topics**: Matplotlib, Seaborn, Plot Types, Advanced Techniques

Comprehensive guide to data visualization using Python's most popular libraries:
- **Time Series**: Line plots, moving averages, decomposition
- **Scatter Plots**: Basic, colored, regression, density plots
- **Heatmaps**: Correlation matrices with different styling
- **Distribution Analysis**: Histograms, box plots, violin plots, Q-Q plots
- **3D Visualizations**: Surface plots, wireframes, contour plots
- **Advanced Techniques**: Multi-panel figures, publication-quality plots

**Key Features**:
- 15+ different plot types demonstrated
- Best practices for data visualization
- Color theory and styling guidelines
- Publication-ready examples

### 3. statistical_analysis.ipynb
**Topics**: Hypothesis Testing, Regression, Time Series, Bayesian Statistics

Complete statistical analysis workflow from data exploration to inference:
- **Descriptive Statistics**: Data exploration and visualization
- **Hypothesis Testing**: T-tests, ANOVA, chi-square tests
- **Regression Analysis**: Linear, multiple, logistic regression
- **Time Series Analysis**: ARIMA modeling and forecasting
- **Bayesian Statistics**: Bayesian inference and credible intervals

**Key Features**:
- Real-world dataset examples
- Step-by-step statistical procedures
- Model interpretation and validation
- Comparison of frequentist vs Bayesian approaches

## Compilation Workflow

### Automatic Compilation
To compile all notebooks into markdown for Zola:

```bash
python scripts/compile_notebooks.py
```

### Compile Specific Notebook
To compile a single notebook:

```bash
python scripts/compile_notebooks.py --notebook mathematical_concepts.ipynb
```

### Clean and Recompile
To clean the output directory and recompile:

```bash
python scripts/compile_notebooks.py --clean
```

## Output Structure

Compiled notebooks are placed in `../zdocs/content/compiled_notebooks/` with:
- **Markdown files**: Each notebook becomes a `.md` file with Zola front matter
- **Assets**: Images and plots are extracted and stored in subdirectories
- **Metadata**: Automatic title extraction, tagging, and execution statistics

### Zola Front Matter
Each compiled notebook includes TOML front matter:

```toml
+++
title = "Notebook Title"
description = "Generated from Jupyter notebook"
weight = 0
draft = false
template = "page.html"
in_search_index = true

[extra]
notebook_source = "original_notebook.ipynb"
generated_date = "2024-03-22 10:30:00"
execution_time = "45.23s"
cell_count = 42
+++
```

## Dependencies

The notebooks require the following Python packages (already installed via `uv add`):

```bash
jupyter          # Jupyter notebook environment
papermill        # Notebook execution engine
nbconvert        # Notebook conversion to markdown
numpy            # Numerical computing
matplotlib       # Plotting library
pandas           # Data manipulation
scipy            # Scientific computing
seaborn          # Statistical visualization
```

## Development Workflow

### 1. Creating New Notebooks
1. Create new `.ipynb` files in this directory
2. Use the existing notebooks as templates for structure and style
3. Include markdown cells with explanations and LaTeX notation
4. Test all code cells for proper execution

### 2. Style Guidelines
- **Markdown Cells**: Include clear explanations and mathematical notation
- **Code Cells**: Add comments and follow PEP 8 style
- **Plots**: Use consistent styling with seaborn themes
- **LaTeX**: Use proper notation for mathematical expressions
- **Structure**: Organize with clear section headers

### 3. Testing Notebooks
Before compiling, ensure notebooks:
- Execute without errors
- Have clear, informative outputs
- Include proper documentation
- Generate meaningful visualizations

## Git Configuration

These notebooks are configured to use a Git filter that strips output when committing:

```bash
# In .git/config
[filter "strip-notebook-output"]
    clean = "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR"
    smudge = "cat"
    required

# In .git/info/attributes
*.ipynb filter=strip-notebook-output
```

This keeps the repository size small while preserving the notebook code and structure.

## Integration with Zola

The compiled notebooks integrate seamlessly with the Zola documentation site:

1. **MathJax Support**: Mathematical notation renders properly
2. **Image Handling**: Plots and figures are automatically extracted and referenced
3. **Search Integration**: Notebooks are included in the site search index
4. **Navigation**: Can be linked from other documentation pages
5. **Theme Integration**: Uses the site's MATbook theme for consistent styling

## Performance Considerations

- **Sequential Execution**: Notebooks are processed one at a time to avoid resource exhaustion
- **Memory Management**: Temporary files are cleaned up after processing
- **Error Handling**: Failed notebooks don't stop the entire compilation process
- **Progress Indication**: Real-time feedback during compilation

## Troubleshooting

### Common Issues

1. **Kernel Errors**: Ensure all required packages are installed
2. **Memory Issues**: Restart kernel if notebooks consume too much memory
3. **Path Issues**: Check that relative paths work correctly
4. **Compilation Errors**: Review error messages for specific issues

### Debug Mode

For detailed debugging, modify the compilation script to enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

When adding new notebooks:

1. Follow the established structure and style
2. Include comprehensive documentation
3. Test thoroughly before committing
4. Update this README with new content
5. Consider adding relevant tags for categorization

## Resources

- [Jupyter Documentation](https://jupyter.org/documentation)
- [Papermill Documentation](https://papermill.readthedocs.io)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)
- [Zola Documentation](https://www.getzola.org/documentation/)
