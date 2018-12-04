#!/usr/bin/python
# encoding:utf-8
import requests
import cgi


HOST = "www.lugaralgum.com"
BASE_HTML_CONTENT = """
<html>
  <head>
    <title>TermaTres Redirect</title>
    <meta charset="UTF-8">
  </head>
  <body>{}</body>
</html>
"""


class ResultParser(object):

    def __init__(self, term_code, result):
        self.term_code = term_code
        self.result = result

    @property
    def term_id(self):
        return self.result['result']['term']['term_id']

    @property
    def term_string(self):
        return self.result['result']['term']['string']

    @property
    def term_url(self):
        path = "/tematres/vocab/index.php?tema={}".format(self.term_id)
        return 'http://' + HOST + path


class OutputFormatter(object):

    def __init__(self, term_code, result=None):
        self.term_code = term_code
        self.result = result

    def print_output(self):
        if self.result:
            new_location = "Location:{}".format(self.result.term_url)
            print new_location
            print
        else:
            print "Content-type: text/html"
            print
            self.display_error_message()

    def display_error_message(self):
        # html body
        vocab_url = "http://" + HOST + '/tematres/'
        messages = {
            'pt': {
                'title': 'Erro no redirecionamento',
                'not_found': 'O termo buscado "{}" não pode ser encontrado.'.format(self.term_code),
                'bad_request': 'É necessário informar o parâmetro term_code para finalizarmos a busca.',
                'final_message': '<a href="{}">Clique aqui</a> para consultar o servidor desse vocabulário manualmente.'.format(vocab_url),
            },
            'eng': {
                'title': 'Redirect error',
                'not_found': 'The search term "{}" does not exist.'.format(self.term_code),
                'bad_request': 'You have to inform the parameter term_code to perform your search',
                'final_message': '<a href="{}">Click here</a> to manually search in the vocabulary\'s server.'.format(vocab_url),
            },
            'esp': {
                'title': 'Término no encontrado',
                'not_found': 'El término buscado "{}" no pudo ser encontrado.'.format(self.term_code),
                'bad_request': 'Es necesario indicar el parámetro term_code para finalizar la búsqueda.',
                'final_message': '<a href="{}">Clic aquí</a> para consultar el servidor de ese vocabulario manualmente.'.format(vocab_url),
            }
        }

        body = ''
        keys = ['pt', 'eng', 'esp']
        for language in keys:
            data = messages[language]
            body += "<h2>{}</h2>".format(data['title'])
            if not term_code:
                body += "<p>{}</p>".format(data['bad_request'])
            else:
                body += "<p>{}</p>".format(data['not_found'])

            body += '<p>{}</p><hr>'.format(data['final_message'])

        print BASE_HTML_CONTENT.format(body)


def get_term_info(term_code):
    path = '/tematres/vocab/api/fetchCode/{}/json'.format(term_code)
    url = 'http://' + HOST + path
    response = requests.get(url)

    if not response.ok:
        return None

    try:
        content = response.json()
        if 'result' in content:
            return ResultParser(term_code, response.json())
    except ValueError:
        # no caso de resultados não encontrados, o servidor PHP nos retorna um XML vazio ao invés de um JSON
        return None


form = cgi.FieldStorage()
term_code = form.getvalue('term_code') or ''
info = get_term_info(term_code)

output = OutputFormatter(term_code, info)
output.print_output()
