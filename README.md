# pandasAi_to_pandas

A brief description of your project.

## Prerequisites

Before you begin, ensure you have the following installed:

* [pyenv](https://github.com/pyenv/pyenv) for Python version management.
* [Poetry](https://python-poetry.org/) for dependency management.
* [direnv](https://direnv.net/) for automatic environment loading (recommended).

## Setup Instructions

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repo-url>
    cd pandasAi_to_pandas
    ```
    If you just created the project locally with this script, you are already in the project directory.

2.  **Navigate to the project directory:**
    If you are not already there:
    ```bash
    cd path/to/pandasAi_to_pandas
    ```

3.  **Environment Activation:**
    * **Using direnv (Recommended):**
        If you have `direnv` installed and hooked into your shell, it should automatically activate the Python version specified in `.python-version` and the Poetry virtual environment when you `cd` into the directory.
        If it's the first time, you might need to run:
        ```bash
        direnv allow .
        ```
    * **Manual Activation with Poetry:**
        If you are not using `direnv`, you can activate the Poetry shell with:
        ```bash
        poetry shell
        ```
        And ensure pyenv is using the correct version:
        ```bash
        pyenv activate 3.11.6
        ```

4.  **Install dependencies:**
    Use the Makefile command for convenience:
    ```bash
    make install-dev
    ```
    Or directly with Poetry:
    ```bash
    poetry install
    ```

5.  **(Optional) Configure environment variables:**
    The project uses a `.env` file for local environment variables. A sample `.env` file is created by the init script. You can customize it as needed. This file is ignored by Git.
    ```bash
    # Example: Edit .env
    # SECRET_KEY=my_new_secret
    # DATABASE_URL=postgresql://user:pass@host:port/mydb
    ```

## Project Structure

-   `src/`: Contains the main source code for your project, typically following the `src-layout`.
-   `tests/`: Contains tests for your project.
-   `.envrc`: Configuration file for `direnv` to automatically manage the shell environment.
-   `.python-version`: Specifies the Python version for the project, managed by `pyenv`.
-   `pyproject.toml`: Defines project metadata, dependencies, and tool configurations for Poetry.
-   `poetry.lock`: Records the exact versions of all dependencies.
-   `Makefile`: Provides convenient shortcuts for common development tasks (e.g., `make install-dev`, `make test`).
-   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
-   `LICENSE`: Contains the project's license information (MIT by default).
-   `.env`: Stores local environment variables (e.g., API keys, database URLs). Not committed to Git.

## Common Development Commands (via Makefile)

-   `make help`: Display available Makefile commands.
-   `make install-dev`: Install all project dependencies, including development tools.
-   `make test`: Run automated tests using `pytest`.
-   `make lint`: Check code for style issues (`flake8`) and formatting (`black --check`).
-   `make format`: Automatically format code using `black`.
-   `make clean`: Remove temporary build artifacts, caches, and compiled files.
-   `make run`: (Placeholder) Run the main application. You'll need to configure this.

## Running the Application

You can run the web application in several ways:

### 1. Using the run script

```bash
python run_app.py
```

### 2. As a module

```bash
python -m src.pandasai_to_pandas
```

### 3. Using Poetry

```bash
poetry run python run_app.py
```

### Environment Variables

The application requires the following environment variables to be set in a `.env` file:

```
DEEPSEEK_API_KEY="sk-your_proxy_key_here"
DEEPSEEK_API_BASE="https://dseek.aikeji.vip/v1/"
```

Optional environment variables:
```
HOST="127.0.0.1"  # Web server host
PORT=5000         # Web server port
DEBUG=False       # Debug mode
```

## Web Interface Features

The web interface provides the following features:

1. **Model Selection**: Choose between `deepseek-chat` and `deepseek-r1` models (控制台会显示已选择的模型)
2. **File Upload**: Drag and drop or select a data file for analysis
3. **多种文件格式支持**: 支持 CSV, Excel (.xlsx, .xls), JSON, Parquet, Feather, Pickle 等格式
4. **Natural Language Query**: Enter a description of the pandas operation you want
5. **Test Button**: Test the model with a pre-defined query
6. **Code Generation**: View the generated pandas code with syntax highlighting
7. **Copy Feature**: Copy the generated code with one click
8. **History**: View and reuse up to 15 previous queries
9. **Clear Functions**: Clear the form, output, and history

## Example Usage

1. Select the model (e.g., `deepseek-chat`)
2. Click "测试模型" to quickly test the selected model with a sample query
3. Upload a data file or use the sample data
4. Enter a query like "找出销量最高的产品类别并绘制柱状图" (Find the highest-selling product category and plot a bar chart)
5. Click "生成代码" (Generate Code)
6. View and copy the generated pandas code

## Contributing

*(If you plan to have others contribute, add guidelines here.)*

---
Generated by init_pyproj.sh script.
