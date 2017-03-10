requirejs.config({
    'baseUrl': '/js/lib',
    'paths': {
        'obstool': '../obstool',
        'data': '../data/'
    }
});

requirejs(['obstool/main']);
