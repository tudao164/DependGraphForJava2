# Java Dependency Graph Generator

This project is an enhanced Java dependency graph generator that analyzes Java source code to create a visual dependency graph using Graphviz. It generates an interactive HTML interface with an image map, allowing users to view and edit the dependency graph dynamically. The tool supports features like hiding/showing nodes and edges, adding custom nodes and edges, and changing node colors.

## Features

- **Java Code Analysis**: Scans Java source files to identify classes, imports, and method calls.
- **Graph Generation**: Creates a Graphviz DOT file and a corresponding PNG image representing the dependency graph.
- **Interactive HTML Interface**: Generates an HTML page with an image map for interactive graph exploration.
- **Graph Editing**: Supports dynamic graph modifications via a web interface, including:
  - Adding/deleting nodes and edges
  - Hiding/showing nodes and edges
  - Updating edge labels (method calls)
  - Setting/resetting node colors
- **Web Server**: Runs a local web server to serve the interactive HTML interface and handle API requests for graph editing.
- **Metadata Generation**: Produces a JSON file with detailed metadata about the analyzed files and dependencies.

## Requirements

- **Python 3.6+**: Required to run the scripts.
- **Graphviz**: Used for generating the DOT file, PNG image, and image map.
  - Install on:
    - **Ubuntu/Debian**: `sudo apt-get install graphviz`
    - **macOS**: `brew install graphviz`
    - **Windows**: Download from [https://graphviz.org/download/](https://graphviz.org/download/)
- A directory containing Java source files (`.java`) to analyze.
- A web browser for viewing the interactive HTML interface.

## Installation

1. **Clone or Download the Repository**:
   ```bash
   git clone <repository-url>
   cd java_dependency_graph
   ```

2. **Install Graphviz**:
   Ensure Graphviz is installed and accessible from the command line. Verify installation with:
   ```bash
   dot -V
   ```

3. **Prepare the HTML Template**:
   Ensure the `dependency_template3.html` file is present in the project directory. This file is required for generating the interactive HTML interface. A basic template is provided, but you may need to customize it for full interactivity (e.g., adding JavaScript for node/edge interactions).

## Project Structure

```
java_dependency_graph/
├── main.py                   # Entry point for the application
├── analyzer.py               # Contains the EnhancedJavaDependencyAnalyzer class
├── server.py                 # Contains the WebUIServer class for the web interface
├── utils.py                  # Placeholder for utility functions
├── dependency_template3.html  # HTML template for the interactive UI
└── README.md                 # Project documentation
```

- **`main.py`**: Parses command-line arguments, orchestrates analysis, and optionally starts the web server.
- **`analyzer.py`**: Handles Java code analysis, dependency graph generation, and graph editing logic.
- **`server.py`**: Runs a local web server to serve the HTML interface and handle API requests for graph editing.
- **`utils.py`**: Placeholder for future utility functions (currently empty).
- **`dependency_template3.html`**: Template for the interactive HTML interface (must include placeholders: `{IMAGE_FILENAME}`, `{MAP_NAME}`, `{MAP_CONTENT}`, `{METADATA_JSON}`).

## Usage

1. **Run the Script**:
   Analyze a directory of Java source files and generate the dependency graph:
   ```bash
   python3 main.py /path/to/java/source
   ```

   This will:
   - Analyze all `.java` files in the specified directory.
   - Generate output files: `dependencies.dot`, `dependencies.png`, `dependencies.map`, `dependencies.html`, and `dependencies_metadata.json`.
   - Print a summary of the analysis.

2. **Launch the Web Interface**:
   To start the web server and open the interactive HTML interface in a browser:
   ```bash
   python3 main.py /path/to/java/source --web
   ```

   The web server will start at `http://localhost:8000/dependencies.html` (default port: 8000).

3. **Command-Line Options**:
   ```bash
   python3 main.py --help
   ```
   - `source_dir`: Path to the directory containing Java source files (required).
   - `--output, -o`: Output DOT file name (default: `dependencies.dot`).
   - `--web, -w`: Automatically start the web server and open the browser.
   - `--port, -p`: Port for the web server (default: 8000).

4. **Example**:
   ```bash
   python3 main.py ./java_project --web --port 8080
   ```
   - Analyzes Java files in `./java_project`.
   - Generates output files in the current directory.
   - Starts the web server on port 8080 and opens the browser.

5. **Output Files**:
   - `dependencies.dot`: Graphviz DOT file defining the dependency graph.
   - `dependencies.png`: PNG image of the graph.
   - `dependencies.map`: Image map for the HTML interface.
   - `dependencies.html`: Interactive HTML page with the graph and editing controls.
   - `dependencies_metadata.json`: Metadata about the analyzed files and dependencies.

6. **Graph Editing**:
   - Use the web interface to:
     - Add/delete custom nodes and edges.
     - Hide/show nodes and edges.
     - Update edge labels (method calls).
     - Change node colors.
   - Changes are sent to the server via API requests and reflected in the generated graph upon regeneration.

## Notes

- **HTML Template**: The `dependency_template3.html` file must exist in the project directory. If missing, the script will fail to generate the HTML output. A basic template is provided in the documentation, but you may need to enhance it with JavaScript for full interactivity.
- **Graphviz Dependency**: Ensure Graphviz is installed and the `dot` command is accessible in your system's PATH.
- **Error Handling**: The script checks for the existence of the source directory and Graphviz installation. Errors are printed to the console with instructions for resolution.
- **Extensibility**: The `utils.py` file is a placeholder for additional helper functions. You can extend it for tasks like custom parsing or logging.

## Troubleshooting

- **Graphviz Not Found**:
  - Ensure Graphviz is installed and the `dot` command is available.
  - Reinstall Graphviz or check your PATH environment variable.
- **Template File Missing**:
  - Verify that `dependency_template3.html` exists in the project directory.
  - Use the provided basic template or create your own with the required placeholders.
- **Web Server Fails to Start**:
  - Check if the specified port (default: 8000) is in use.
  - Use the `--port` option to specify a different port.
- **No Java Files Found**:
  - Ensure the specified source directory contains valid `.java` files.
  - Check the directory path for typos.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please include tests and update documentation as needed.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or issues, please open an issue on the repository or contact the maintainer.