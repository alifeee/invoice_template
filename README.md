# Invoice Template

Template for making an invoice. Outputs HTML and PDF. Uses TOML for information, e.g.,

```toml
id = "001"
amount = "300"
issue_date = "2023-11-30"
due_date = "2023-12-30"

[from]
name = "alifeee"

[to]
name = "Garibaldi"

[[items]]
title = "Biscuit Generation"
time_h = "1.5"
charge = "150"

# ...
```

...creates...

![Screenshot of PDF invoice, filled in with example data.](images/invoice.png)

## Commands

### Install dependencies

```bash
py -m venv env
pip install -r requirements.txt
playwright install
```

### Make Invoice

First, add `invoice.toml` to the root of the repository, that looks like [`invoice.example.toml`](./invoice.example.toml). Then,

```bash
python build.py
```

### Hot reload

This watches the template file and the TOML file, and rebuilds the build files when they change. For proper hot-reload, use VSCode's [live server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension on the output `build/invoice.html` file.

```bash
python build.py --hot
```
