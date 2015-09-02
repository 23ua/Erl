### Erl (Erlang Tests & Code Completion); Fork of fork of SublimErl for ST3 (:

---

### Overview

Erl is a plugin for the text editor [Sublime Text 3](http://www.sublimetext.com). It allows you to:

* Benefit from **Code Completion** (all Erlang libs + your current project)
* Allows you to **Auto-Indent** your Erlang code
* Run **Eunit** tests (all tests for module/single test)
* Run **Common Tests** (all tests for module)
* Run **Dialyzer** tests (single module)
* **Goto any exported function** of your project easily
* Access **man pages** from the text editor

All within your test editor. A brief feature introduction video can be seen [here](http://www.youtube.com/watch?v=KIzxbjlHmu0).

---

### Usage

* **Code Completion**: Just type and select available options
* **Auto-Indenting**: hit `Command-Option-L` to auto-intent an entire file
* Run **single Eunit**: position your cursor anywhere **within** your test function and hit `Command-Shift-F8`
* Run **all Eunit tests** in file: position your cursor **outside** any test function and hit `Command-Shift-F8`
* Run **all CT tests** in file: view the file and hit `Command-Shift-F8`
* Run **Dialyzer** on file: view the file and hit `Command-Shift-F9`
* Re-Run the **previous test**: hit `Command-F8` ( you do not need to be viewing the test to launch it )
* View **Common Tests results** in browser: hit `Command-Option-F8` (OSX) | `Command-Alt-F8` (Linux/Win)
* **Goto any exported function** of your project easily: hit `Command-Option-p` (OSX) | `Command-Alt-p` (Linux/Win) and select a function
* To access **man pages**: hit `Command-Option-i` (OSX) | `Command-Alt-i` (Linux/Win) and select a module

---

### Installation

Erl currently supports only on **OSX** and **Linux** (may work in Windows, but not tested). There are 3 ways to install it:

##### 1. Sublime Package Control

Erl's latest stable versions are pushed automatically to the package control.

##### 2. From source
Go to your Sublime Text 3 `Packages` directory:

* OS X: `~/Library/Application Support/Sublime Text 3/Packages`
* Linux: `~/.Sublime Text 3/Packages/`

and clone the repository using the command below:

```bash
$ git clone https://github.com/23ua/Erl.git
```

---

### Configuration

Erl needs and will try to detect the paths of the following executables: **rebar**, **erl**, **escript** and **dialyzer**. If it doesn't succeed to find those, or if you prefer to manually configure these path, you can set them in the `Erl.sublime-settings` file, located in the `Erl` plugin directory.

---

### Dependencies

To use Erl, you need to have:

* [Sublime Text 3](http://www.sublimetext.com)
* [Erlang](http://www.erlang.org/download.html)
* [Rebar](https://github.com/rebar/rebar)
* [Erlang man pages](http://www.erlang.org/download.html) (optional)

To unleash the full power of the plugin, you will also need to comply to:

* OTP standards (i.e. have your project defined according to [OTP Directory Structure](http://www.erlang.org/doc/design_principles/applications.html#id73730)).
* [Rebar's conventions](https://github.com/basho/rebar/wiki/Rebar-and-OTP-conventions).

TL;DR: it basically means to organize your project structure using:

```
-- myproject
   |-- ebin
   |-- src
       |-- myproject.app.src
   |-- test
   |-- ...
```

or, for example, a more complex project structure defined in rebar.conf:

```
-- myproject
   rebar.config
   |-- apps
       |-- app1
       |-- app2
   |-- deps
       |-- dep1
       |-- dep2
   |-- ...
```

---

### TODO

* Add snippets
* Add REPL
* Highlight erlang configurations

---

### Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
