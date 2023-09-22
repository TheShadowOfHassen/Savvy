# Savvy
A simple Python3 LanguageTool Wrapper.

Features:
- A module that is similar to LanguageToolPython.
- A Gtk wrapper for the language tool server so you can manage your own Language tool Server. 

# Example:

	import savvy
    l = LanguageToolChecker()
    d = l.check('''Today's is the day you almost mispelled Captain Jack Spawwow!''')
    for i in d:
        print(i.replacements)
    l.close_checker()

This module is licensed, like LanguageTool under the LesserGPL. In this (alpha) version LanguageTool is included.


# TODO
Help us with these features!

- API compatibility to LanguageToolPython
- A package for the server.
