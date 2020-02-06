Flask-Babel-JS
---

Flask extension to add Flask-Babel translations in JS.

## Installation

Install via pip: `pip install flask-babel-js`
Keep in mind that this extension expects you to have
[`flask_babel`](https://github.com/python-babel/flask-babel) set-up
correctly beforehand.

## Usage

You can initialize this extension both directly and using the application
factory pattern:

``` python
from flask import Flask
from flask_babel import Babel
from flask_babel_js import BabelJS

# Initializing directly:
app = Flask(__name__)
babel = Babel(app)
babel_js = BabelJS(app)

# Initializing via application factory pattern:
babel = Babel()
babel_js = BabelJS()


def create_app():
    app = Flask(__name__)

    babel.init_app(app)
    babel_js.init_app(app)

    return app
```

When the extension is initialized, a new route with the name of `babel_catalog`
is added to the list of routes. This is a JavaScript file which contains all
translations in your current locale. It also includes a very basic
`gettext`-like API which you can use. It is compatible with the `javascript`
extraction method of [`Babel`](https://github.com/python-babel/babel).

Add this to your `babel.cfg` to extract Javascript translation strings:

``` ini
[javascript:app/static/*.js]
encoding = utf-8
extract_messages=_,gettext,ngettext
```

To include the translation catalog and functions, insert the following
inside your Jinja templates:

``` jinja
<script src="{{ url_for("babel_catalog") }}"></script>
```

Afterwards, you can use all the functions available in the [Javascript
API](#javascript-api).

Example usage in Javascript:

``` javascript
// Translate a string
var s = _("Some untranslated text");
// Translate a string with format values
var s2 = _("Hello, %(name)s!", { name: "John" });
// Translate a string with plural forms
var s3 = ngettext("%(n)d item was deleted.", "%(n)d items were deleted.", n, { n: n });
// You can access all these functions through the babel object:
// babel.gettext, babel.ngettext
```

## Python API

### `flask_babel_js.BabelJS(app=None, view_path="/_jstrans.js")`

Initializes the extension object.

Parameters:
 - `app`: The Flask application. Can be `None` if you are using the application
   factory pattern.
 - `view_path`: The path for the catalog URL. Defaults to `"/_jstrans.js"`.

#### `init_app(app)`

Initialize an application with the extension object.

Parameters:
 - `app`: The Flask application.

#### `catalog_view()`

The catalog view which provides the JavaScript code for the catalog. You don't
need to use this directly.

## Javascript API

### `window.babel`

The main BabelJS object.

#### `catalog`

All gettext messages for the current locale are in this object. The keys are
the original arguments passed to gettext and the value is the translated
version. If the translated text has a plural form, the value is an array of the
plural forms.

#### `format(text, variables)`

Formats text using Python percent-formatting. Currently only supports `s`, `d`,
and `f` as format types. Also expects a format name. For extensions, only left
padding is supported.

Parameters:
 - `text`: A Python-format string.
 - `variables`: An object containing values for the format specifiers.

#### `gettext(text, variables)`

Translates a string.

This function is available globally as `gettext` and `_`.

Parameters:
 - `text`: The untranslated string.
 - `variables`: An object containing values for the format specifiers.

#### `ngettext(text, plural_text, n, variables)`

Translates a string with plural forms based on a value.

This function is available globally as `ngettext`.

Parameters:
 - `text`: The untranslated string.
 - `plural_text`: The untranslated string in plural form.
 - `n`: The amount of items by which the form is selected.
 - `variables`: An object containing values for the format specifiers.

#### `plural(n)`

Gets the plural form ID corresponding to the number of items for this locale.

Parameters:
 - `n`: The number of items.

NOTE: This function may not exist if `Plural-Forms` is not specified in the
gettext metadata in the locale.

## License

&copy; 2020 Efe Mert Demir. This software is licensed under the 3-Clause BSD
License, a copy of which can be found in [LICENSE](https://github.com/emdemir/Flask-Babel-JS/blob/master/LICENSE).
