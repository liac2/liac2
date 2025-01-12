document.addEventListener('DOMContentLoaded', () => {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('', '', ''));

  // Send mail
  document.querySelector('#compose-form').onsubmit = () => {

    // Get input data
    data = {};
    data.recipients = document.querySelector('#compose-recipients').value;
    data.subject = document.querySelector('#compose-subject').value;
    data.body = document.querySelector('#compose-body').value;

    // Prepare data
    data.recipients.split(' ').join(',');

    // Send mail to server
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: data.recipients,
          subject: data.subject,
          body: data.body
      })
    })
    .then(response => response.json())
    .then(result => {
    })
    .then(() => {
      load_mailbox('sent');
    });

    return false;
  };

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email(recipients, subject, body) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelectorAll('.single-email-view').forEach(div =>{
    div.remove();
  });

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelectorAll('.single-email-view').forEach(div => {
    div.remove();
  });

  // Show the mailbox name
  let old = document.querySelector('#emails-view');
  old.innerHTML = '';
  old.innerHTML += `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load emails on inbox, sent, archive 
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    console.log(emails);

    // Create html for email
    for (let mail of emails) {
      let entry = document.createElement('a'); 
      if (mail.read === true) {
        entry.className = 'list-group-item list-group-item-action list-group-item-light bg-light';
      }
      else {
        entry.className = 'list-group-item list-group-item-action';
      }
      entry.dataset.id = mail.id;
      entry.href = '#';
      entry.ariaCurrent = 'true';
      entry.innerHTML = `<div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">${mail.subject}</h5>
            <small>${mail.timestamp}</small>
            </div>
            <p class="mb-1">${mail.sender}</p>`;

      // View single email
      entry.addEventListener('click', event => {

        // Setup page
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelectorAll('.single-email-view').forEach(element =>{
          element.remove();
        });

        // render components of mail
        let view = document.createElement('div');
        view.className = 'single-email-view';
        view.innerHTML = `
        <div class="row">
          <div class="col-10">
            <h1>${mail.subject}</h1>
            <h2 class="h5">From: ${mail.sender}</h2>
            <h2 class="h5">To: ${mail.recipients}</h2>
          </div>  
          <div class="col-2 sidebar">
            <div class="header-sidebar">
              <small class="">${mail.timestamp}</small>
              <button type="button" id="archive" class="btn btn-secondary">
                <i class="bi bi-archive"></i>
              </button>
            </div> 
             <div class="">
              <button type="button" id="reply" class="btn btn-secondary">
              <i class="bi bi-reply"></i>Reply
              </button>
            </div>
          </div>  
        </div>
          
        <hr>
        <p>${mail.body}</p>`;

        document.querySelector('.container').append(view);

        // Mark mail on server as read
        fetch(`/emails/${mail.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        });

        // Reply btn
        document.querySelector('#reply').onclick = () => {
          let subject = '';
          if (!mail.subject.startsWith('Re: ')) {
            subject = 'Re: ' + mail.subject;
          } else {
            subject = mail.subject;
          }
          let body = `On ${mail.timestamp} ${mail.sender} wrote:\n${mail.body}\n`;
          compose_email(mail.sender, subject, body);
        };
        
        // Archive btn
        document.querySelector('#archive').onclick = () => {
          
          // Get current archived state
          fetch(`/emails/${mail.id}`)
          .then(response => response.json())
          .then(new_mail => {

            // Set opposite state
            fetch(`/emails/${mail.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: !new_mail.archived
              })
            })
            // Load inbox
            .then(() => {
              load_mailbox('inbox');
            });
          });
        };

      });

      old.append(entry);
    }
  });
}