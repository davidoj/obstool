define(["data/config", "data/templates", "data/version"],
function(config, templates, version) {

config.router = {
    'base_url': ''
}

config.template = {
    'templates': templates,
    'defaults': {
        'version': version,
        'date': function() {
            var date = new Date();
            return (
                date.getFullYear() + '-' +
                (date.getMonth() < 9 ? '0' : '') +
                (date.getMonth() + 1) + '-' +
                (date.getDate() <= 9 ? '0' : '') +
                date.getDate()
            );
}
    }
}

config.store = {
    'service': config.router.base_url,
    'defaults': {'format': 'json'}
}


config.outbox = {};

config.transitions = {
    'default': "slide",
    'save': "flip"
};

return config;

});
