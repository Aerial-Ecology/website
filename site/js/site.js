// Mobile menu
(function () {
  const nav = document.getElementById('nav');
  const btn = document.querySelector('.menu-toggle');
  if (nav && btn) {
    btn.addEventListener('click', function () {
      const open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
      btn.textContent = open ? 'Close' : 'Menu';
    });
  }
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();

// Enquiry form.
// The endpoint comes from FORM_ENDPOINT in src/build.py (Web3Forms). With an endpoint,
// enquiries are posted directly and a confirmation is shown. Without one, the form falls back to opening a
// pre-filled email so no enquiry is lost.
(function () {
  const form = document.getElementById('enquiry');
  if (!form) return;
  const status = document.getElementById('form-status');
  const button = form.querySelector('button[type="submit"]');

  function summary(data) {
    const services = data.getAll('service').join(', ') || 'Not specified';
    return [
      'Name: ' + data.get('name'),
      'Organisation: ' + (data.get('organisation') || '-'),
      'Email: ' + data.get('email'),
      'Phone: ' + (data.get('phone') || '-'),
      'Site location: ' + (data.get('location') || '-'),
      'Services: ' + services,
      'Survey window: ' + (data.get('timing') || '-'),
      '',
      data.get('message')
    ].join('\n');
  }

  function confirm() {
    form.classList.add('sent');
    status.className = 'form-status ok';
    status.innerHTML = '<strong>Thank you, your enquiry has been sent.</strong>We’ll reply by email. If it’s urgent, email info@aerial-ecology.co.uk.';
    status.focus();
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    // Spam filtering is left to the form service (it discards submissions that tick the hidden botcheck box),
    // so a real enquiry is never dropped silently in the browser.
    data.set('service', data.getAll('service').join(', ') || 'Not specified');
    const endpoint = form.dataset.endpoint;
    status.className = 'form-status';

    if (!endpoint) {
      const subject = 'Project enquiry from ' + data.get('name');
      window.location.href = 'mailto:info@aerial-ecology.co.uk?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(summary(new FormData(form)));
      status.textContent = 'Your email app should open with the enquiry filled in. If it doesn’t, email info@aerial-ecology.co.uk directly.';
      return;
    }

    status.textContent = 'Sending…';
    button.disabled = true;
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(data)),
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' }
      });
      const result = await res.json();
      if (!res.ok || !result.success) throw new Error(result.message || res.status);
      form.reset();
      confirm();
    } catch (err) {
      status.classList.add('err');
      status.textContent = 'Sorry, the form couldn’t send just now. Please try again, or email info@aerial-ecology.co.uk and we’ll pick it up.';
    } finally {
      button.disabled = false;
    }
  });
})();
