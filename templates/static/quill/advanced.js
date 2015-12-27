var editor;

//_ = Quill.require('lodash');

editor = new Quill('.advanced-wrapper .editor-container', {
  modules: {
    'toolbar': {
      container: '.advanced-wrapper .toolbar-container'
    },
    'link-tooltip': true,
    'image-tooltip': true,
    'multi-cursor': true
  },
  styles: false,
  theme: 'snow'
});

$('.ql-editor').on('focus', function(){
  if ($('.placeholder').length) {
    editor.setHTML('');
    editor.focus();
  }
});

$('.ql-editor').on('blur', function(){
  setTimeout(function(){
    console.log(editor.getLength());
    if (editor.getLength() <= 1) {
      editor.setHTML('<label class="placeholder">Start Writing here ...</label>');
    }
  }, 500);
});

editor.on('text-change', function(delta, source) {
  if (source == 'api') {
    console.log("An API call triggered this change.");
  } else if (source == 'user') {
    console.log("A user action triggered this change.");
  }
  var post = editor.getHTML();
  $('#post').val(post);
});