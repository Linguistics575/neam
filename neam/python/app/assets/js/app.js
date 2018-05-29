$(() => {
  let elements = {
    progress_bar: $('#progress-bar'),
    button: $('#submit-button'),
    text: $('#info-text')
  };

  elements['progress_bar'].hide();
  elements['text'].hide();

  $('#annotation-form').ajaxForm({
    success(data, textStatus, request) {
      status_url = request.getResponseHeader('Location');
      update_progress(status_url, elements);
    },
    beforeSubmit() {
      elements['progress_bar'].show();
      elements['text'].show();
      elements['button'].addClass('disabled');
    }
  });
});

function update_progress(status_url, elements) {
  $.getJSON(status_url, data => {
    let state = data['state'];

    if (state == 'PENDING' || state == 'PROGRESS') {
      setTimeout(() => {
        update_progress(status_url, elements);
      }, 2000);
    } else {
      window.location = '/download/' + data['result'];
      elements['progress_bar'].hide();
      elements['text'].hide();
      elements['button'].removeClass('disabled');
    }
  });
}

