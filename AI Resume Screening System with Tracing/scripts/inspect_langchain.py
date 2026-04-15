import langchain, pkgutil
print('version', getattr(langchain, '__version__', '?'))
print('modules:')
for finder, name, ispkg in pkgutil.iter_modules(langchain.__path__):
    print('-', name, 'pkg' if ispkg else '')

# try common import paths
for path in ['langchain.llms', 'langchain.llms.openai', 'langchain.llms.openai.OpenAI', 'langchain.openai', 'langchain.chat_models', 'langchain.llm']:
    try:
        m = __import__(path, fromlist=['*'])
        print('import ok:', path, '->', getattr(m, '__name__', str(m)))
    except Exception as e:
        print('import fail:', path, '->', e)
