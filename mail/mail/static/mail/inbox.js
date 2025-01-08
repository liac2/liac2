document.addEventListener('DOMContentLoaded', () => {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send mail
  document.querySelector('#compose-form').onsubmit = () => {

    // Get input data
    data = {};
    data.recipients = document.querySelector('#compose-recipients').value;
    data.subject = document.querySelector('#compose-subject').value;
    data.body = document.querySelector('#compose-body').value;

    // Prepare data
    data.recipients.split(' ').join(',');
    console.log(data);

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
        console.log(result);
    });

    // Load 'sent' view
    load_mailbox('sent');

    return false;
  };

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

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
    for (const mail of emails) {
      let entry = document.createElement('a'); 
      if (mail.read === true) {
        entry.className = 'list-group-item list-group-item-action list-group-item-light';
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
      old.append(entry);
    }
  });

  // View single email
  old.childNodes.forEach(mail => {
    mail.addEventListener('click', event => {

      // Hide other emails
      old.innerHTML = '';
      
      // View single email 
      fetch(`/emails/${this.dataset.id}`)
      .then(response => response.json())
      .then(email => {

          // sender, recipients, subject, timestamp, and body.
          div.innerHTML = ``
        });
      

    });
  });
}