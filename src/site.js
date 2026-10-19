(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  if (toggle && header) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.mobile-nav a').forEach(function (a) {
      a.addEventListener('click', function () { header.classList.remove('nav-open'); });
    });
  }
  // Contact form: Web3Forms via fetch when a key is set; otherwise hand off to the mail app.
  var form = document.querySelector('form[data-form]');
  if (form) {
    var key = form.getAttribute('data-key');
    var status = form.querySelector('.form-status');
    var button = form.querySelector('button[type=submit]');
    function val(n) { var el = form.elements[n]; return el ? el.value.trim() : ''; }
    form.addEventListener('submit', function (ev) {
      if (form.elements.botcheck && form.elements.botcheck.checked) { ev.preventDefault(); return; }
      if (!form.checkValidity()) { ev.preventDefault(); form.reportValidity(); return; }
      if (!key) {
        ev.preventDefault();
        var body = ['Name: ' + val('name'), 'Company: ' + val('company'), 'Email: ' + val('email'),
          'Phone: ' + (val('phone') || '-'), 'Topic: ' + val('topic'), '', val('message')].join('\n');
        window.location.href = 'mailto:info@apexscm.us?subject=' + encodeURIComponent('Enquiry via apexscm.us: ' + val('topic')) + '&body=' + encodeURIComponent(body);
        return;
      }
      if (!window.fetch) return; // plain POST + redirect to /contact/thanks/
      ev.preventDefault();
      button.disabled = true; status.textContent = 'Sending\u2026';
      var data = { access_key: key };
      Array.prototype.forEach.call(form.elements, function (el) { if (el.name && el.name !== 'botcheck' && el.name !== 'redirect') data[el.name] = el.value; });
      fetch('https://api.web3forms.com/submit', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json(); })
        .then(function (res) { if (!res.success) throw new Error(res.message || 'failed'); form.classList.add('sent'); form.scrollIntoView({ behavior: 'smooth', block: 'start' }); })
        .catch(function () { status.textContent = 'Something went wrong. Please email info@apexscm.us directly.'; button.disabled = false; });
    });
  }

  var reveals = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  function showAll() { reveals.forEach(function (el) { el.classList.add('in'); }); }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    reveals.forEach(function (el) { io.observe(el); });
    // Fail-safe: never leave content hidden (print, odd viewports, slow observers).
    window.setTimeout(showAll, 1500);
    window.addEventListener('beforeprint', showAll);
  } else {
    showAll();
  }
})();
