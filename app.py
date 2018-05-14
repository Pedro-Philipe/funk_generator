import pickle
import random

from collections import defaultdict

from flask import Flask, request, jsonify
from flask_cors import CORS

from model.sample_generator import create_sample


app = Flask(__name__)
CORS(app)


# load the model
default_args = {
    'use_checkpoint': True,
    'embedding_size': 300,
    'num_layers': 3,
    'num_units': 728
}

all_args = {
    'checkpoint_path': 'checkpoint',
    'index2word_path': 'data/song_dataset/index2word.pkl',
    'word2index_path': 'data/song_dataset/word2index.pkl',
    'vocab_size': 12551,
}
all_args = {**default_args, **all_args}
all_args = defaultdict(int, all_args)

kondzilla_args = {
    'checkpoint_path': 'kondzilla_checkpoint',
    'index2word_path': 'kondzilla/song_dataset/index2word.pkl',
    'word2index_path': 'kondzilla/song_dataset/word2index.pkl',
    'vocab_size': 2192,
}
kondzilla_args = {**default_args, **kondzilla_args}
kondzilla_args = defaultdict(int, kondzilla_args)

proibidao_args = {
    'checkpoint_path': 'proibidao_checkpoint',
    'index2word_path': 'proibidao/song_dataset/index2word.pkl',
    'word2index_path': 'proibidao/song_dataset/word2index.pkl',
    'vocab_size': 1445,
}
proibidao_args = {**default_args, **proibidao_args}
proibidao_args = defaultdict(int, proibidao_args)

ostentacao_args = {
    'checkpoint_path': 'ostentacao_checkpoint',
    'index2word_path': 'ostentacao/song_dataset/index2word.pkl',
    'word2index_path': 'ostentacao/song_dataset/word2index.pkl',
    'vocab_size': 2035,
}
ostentacao_args = {**default_args, **ostentacao_args}
ostentacao_args = defaultdict(int, ostentacao_args)

all_sampler = create_sample(all_args)
kondzilla_sampler = create_sample(kondzilla_args)
proibidao_sampler = create_sample(proibidao_args)
ostentacao_sampler = create_sample(ostentacao_args)

def load(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

all_songs = load('generated_songs/generated-all-songs.pkl')
kondzilla_songs = load('generated_songs/generated-all-songs.pkl')
proibidao_songs = load('generated_songs/generated-all-songs.pkl')
ostentacao_songs = load('generated_songs/generated-all-songs.pkl')

def get_song(model_id):
    random_num = random.randint(0, len(all_songs) - 1)

    if model_id == 1:
        return all_songs[random_num]
    elif model_id == 2:
        return kondzilla_songs[random_num]
    elif model_id == 3:
        return proibidao_songs[random_num]
    else:
        return ostentacao_songs[random_num]


# API route
@app.route('/api', methods=['POST'])
def api():
    """API function

    All model-specific logic to be defined in the get_model_api()
    function
    """
    data = request.json
    model_id = data['id']
    prime_words = data['sentence']

    if prime_words == None:
        output_data = get_song(model_id)
    else:
        if model_id == 1:
            output_data = all_sampler(prime_words, html=True)
        elif model_id == 2:
            output_data = kondzilla_sampler(prime_words, html=True)
        elif model_id == 3:
            output_data = proibidao_sampler(prime_words, html=True)
        else:
            output_data = ostentacao_sampler(prime_words, html=True)

    return jsonify(output_data)


@app.route('/')
def index():
    return "Index API"


# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='0.0.0.0', debug=True)
