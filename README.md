# Savvy
A simple Python3 LanguageTool Wrapper

# Example:

    l = LanguageToolChecker()
    d = l.check('''Today's is the day you almost mispelled Captain Jack Spawwow!''')
    for i in d:
        print(i.replacements)
    l.close_checker()

This module is licensed, like LanguageTool under the LesserGPL. In this (alpha) version LanguageTool is included.