define(['wq/app', 'wq/map', 'wq/patterns', 'wq/photos',
        './config',
        'leaflet.draw'],
function(app, map, patterns, photos, config) {

app.use(map);
app.use(patterns);
app.use(photos);

// Anonymous plugin
app.use({
    'onsave': function(item, result) {
        // Parameter is registered as a nested serializer on campaign, and is
        // is also registered separately.  This dual usage is not officially
        // supported by wq (see https://wq.io/docs/nested-forms), so we need to
        // refresh the parameter model whenever a campaign is saved.
        if (item && item.options &&
                item.options.modelConf &&
                item.options.modelConf.name == 'obsform') {
            app.models.item.prefetch();
        }
    }
});

config.presync = presync;
config.postsync = postsync;
app.init(config).then(function() {
    app.jqmInit();
    app.prefetchAll();
});

// Sync UI
function presync() {
    $('button.sync').html("Syncing...");
    $('li a.ui-icon-minus, li a.ui-icon-alert')
       .removeClass('ui-icon-minus')
       .removeClass('ui-icon-alert')
       .addClass('ui-icon-refresh');
}

function postsync(items) {
    $('button.sync').html("Sync Now");
    app.syncRefresh(items);
}

});
