import gettext
import json

from flask import Response
from flask_babel import get_translations


JAVASCRIPT = r"""
    /**
     * Formats text using Python-style formatting specifiers.
     * This function supports strings, integers and floats.
     * @param {string} text - The text
     * @param {object} variables - An object containing the variables for the
     *                 specifiers.
     * @return {string}
     */
    babel.format = function(text, variables) {
        if (typeof variables !== "object") {
            variables = {};
        }

        return text.replace(
            /%\(([a-zA-Z0-9]\w*)\)(\d+)?([a-z])/g,
            function(match, fname, length, type) {
                if (!(fname in variables) || !variables.hasOwnProperty(fname))
                    throw new Error(
                        "Format variable " + fname + " doesn't exist!"
                    );

                var v = variables[fname];
                var output = "";

                if (type === "d") {
                    v = "" + (v|0);
                } else if (type === "f") {
                    v = "" + (+v);
                } else if (type === "s") {
                    v = "" + v;
                } else {
                    throw new Error("Unknown formatting specifier " + type);
                }

                if (length && v.length < length|0) {
                    if (length.charAt(0) === "0" &&
                        (type === "d" || type === "f")) {
                        output += Array((length|0) - v.length).join("0");
                    } else {
                        output += Array((length|0) - v.length).join(" ");
                    }
                }

                output += v;
                return output;
            }
        );
    };

    /**
     * Get some text translated in the current language.
     * @param {string} text - The text
     * @param {object} variables - An object containing the variables for
     *                 formatting.
     * @return {string}
     */
    babel.gettext = function(text, variables) {
        if ((text in babel.catalog) && babel.catalog.hasOwnProperty(text)) {
            return babel.format(babel.catalog[text], variables);
        } else {
            return babel.format(text, variables);
        }
    };

    /**
     * Get some pluralized text translated in the current language.
     * @param {string} text - The text
     * @param {string} plural_text - The text for plural
     * @param {number} n - The amount of items, determines plurality
     * @param {object} variables - An object containing the variables for
     *                 formatting.
     * @return {string}
     */
    babel.ngettext = function(text, text_plural, n, variables) {
        var p;
        if (babel.plural) {
            p = babel.plural(n);
        } else {
            p = p === 1 ? 0 : 1;
        }

        if ((text in babel.catalog) && babel.catalog.hasOwnProperty(text)) {
            return babel.format(babel.catalog[text][p], variables);
        } else {
            return babel.format([text, text_plural][p], variables);
        }
    };
"""


def c2js(plural):
    """Gets a C expression as used in PO files for plural forms and returns a
    JavaScript function that implements an equivalent expression.
    """

    if len(plural) > 1000:
        raise ValueError('plural form expression is too long')

    return "function(n) { return (" + plural + "); }"


class BabelJS(object):
    """
    A Flask extension to provide a translation catalog in Javascript code.
    """

    def __init__(self, app=None, view_path="/_jstrans.js"):
        """Initializes the extension.
        Keyword Arguments:
        app       -- (default None) The Flask application.
        view_path -- (default "_jstrans") The path for the catalog URL.
        """
        self.view_path = view_path

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize an application with this extension.
        Keyword Arguments:
        app -- The Flask application.
        """
        app.add_url_rule(self.view_path, "babel_catalog", self.catalog_view)

    def catalog_view(self):
        js = [
            """"use strict";

(function() {
    var babel = {};
    babel.catalog = """
        ]

        translations = get_translations()
        # Here used to be an isinstance check for NullTranslations, but the
        # translation object that is "merged" by flask-babel is seen as an
        # instance of NullTranslations.
        catalog = translations._catalog.copy()

        for key, value in catalog.items():
            if isinstance(key, tuple):
                text, plural = key
                if text not in catalog:
                    catalog[text] = {}

                catalog[text][plural] = value

        js.append(json.dumps(catalog, indent=4))

        js.append(";\n")
        js.append(JAVASCRIPT)

        metadata = translations.gettext("")
        if metadata:
            for m in metadata.splitlines():
                if m.lower().startswith("plural-forms:"):
                    js.append("    babel.plural = ")
                    js.append(c2js(m.lower().split("plural=")[1]))

        js.append("""

    window.babel = babel;
    window.gettext = babel.gettext;
    window.ngettext = babel.ngettext;
    window._ = babel.gettext;
})();
""")

        resp = Response("".join(js))
        resp.headers["Content-Type"] = "text/javascript"
        return resp
