
  <script>
    /* ── Quiz & Apply it ────────────────────────────────────────────────
       Two practice modes. QUIZ and SCENARIOS are the only authored parts;
       the renderer below is identical on every week page, so a re-sync
       swaps the arrays and leaves the behaviour alone. Progressive
       enhancement: with JS off both panels sit empty and the five synced
       modes are unaffected. */
    (function () {
      'use strict';

      var quizListEl = document.getElementById('quiz-list');
      var scenListEl = document.getElementById('scen-list');
      if (!quizListEl && !scenListEl) return;

      function esc(s) {
        return String(s == null ? '' : s)
          .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;');
      }

      var KEYS = ['A', 'B', 'C', 'D', 'E', 'F'];

      var QUIZ = /*QUIZ*/[]/*END_QUIZ*/;
      var SCENARIOS = /*SCENARIOS*/[]/*END_SCENARIOS*/;

      /* ── Quiz ─────────────────────────────────────────────── */
      if (quizListEl && QUIZ.length) {
        var doneEl = document.getElementById('quiz-done');
        var rightEl = document.getElementById('quiz-right');
        var totalEl = document.getElementById('quiz-total');
        var fillEl = document.getElementById('quiz-fill');
        var verdictEl = document.getElementById('quiz-verdict');
        var resetBtn = document.getElementById('quiz-reset');

        var answered = 0;
        var correct = 0;

        totalEl.textContent = QUIZ.length;

        quizListEl.innerHTML = QUIZ.map(function (q, i) {
          return '<article class="quiz-q">' +
            '<div class="quiz-head">' +
              '<span class="quiz-n">Question ' + (i + 1) + '</span>' +
              (q.topic ? '<span class="term-src">' + esc(q.topic) + '</span>' : '') +
            '</div>' +
            '<p class="quiz-stem">' + esc(q.q) + '</p>' +
            (q.hint
              ? '<details class="reveal"><summary>Hint</summary>' +
                '<div class="reveal-body"><p>' + esc(q.hint) + '</p></div></details>'
              : '') +
            '<div class="opts" role="group" aria-label="Answer options for question ' + (i + 1) + '">' +
              q.options.map(function (o, j) {
                return '<button class="opt" type="button" data-q="' + i + '" data-o="' + j + '">' +
                  '<span class="opt-key" aria-hidden="true">' + KEYS[j] + '</span>' +
                  '<span class="opt-t">' + esc(o.t) + '</span></button>';
              }).join('') +
            '</div>' +
            '<div class="fb-slot" id="fb-' + i + '" role="status" aria-live="polite"></div>' +
            '</article>';
        }).join('');

        var qEls = Array.prototype.slice.call(quizListEl.querySelectorAll('.quiz-q'));

        function paintScore() {
          doneEl.textContent = answered;
          rightEl.textContent = correct;
          fillEl.style.width = (answered / QUIZ.length * 100) + '%';
          if (answered === QUIZ.length) {
            verdictEl.textContent = 'All done — ' + correct + ' of ' + QUIZ.length +
              ' correct. Reread the ones you missed in Summary & visuals, then start over.';
            verdictEl.removeAttribute('hidden');
          } else {
            verdictEl.setAttribute('hidden', '');
          }
        }

        function answer(i, chosen) {
          var q = QUIZ[i];
          var wrap = qEls[i];
          if (wrap.getAttribute('data-answered') === 'true') return;
          wrap.setAttribute('data-answered', 'true');

          var opts = Array.prototype.slice.call(wrap.querySelectorAll('.opt'));
          var rightIdx = -1;
          q.options.forEach(function (o, j) { if (o.ok) rightIdx = j; });

          opts.forEach(function (el, j) {
            el.disabled = true;
            if (j === rightIdx) el.setAttribute('data-state', 'right');
            else if (j === chosen) el.setAttribute('data-state', 'wrong');
            else el.setAttribute('data-state', 'off');
          });

          var isRight = chosen === rightIdx;
          answered++;
          if (isRight) correct++;

          var html = '<div class="fb ' + (isRight ? 'fb--right' : 'fb--wrong') + '">' +
            '<span class="fb-tag">' + (isRight ? 'Correct' : 'Not this one') + '</span>' +
            '<p>' + esc(q.options[chosen].note) + '</p></div>';
          if (!isRight) {
            html += '<div class="fb fb--right">' +
              '<span class="fb-tag">' + KEYS[rightIdx] + ' is the answer</span>' +
              '<p>' + esc(q.options[rightIdx].note) + '</p></div>';
          }
          document.getElementById('fb-' + i).innerHTML = html;
          paintScore();
        }

        quizListEl.addEventListener('click', function (e) {
          var node = e.target;
          while (node && node !== quizListEl && !(node.classList && node.classList.contains('opt'))) {
            node = node.parentNode;
          }
          if (!node || node === quizListEl || node.disabled) return;
          answer(parseInt(node.getAttribute('data-q'), 10), parseInt(node.getAttribute('data-o'), 10));
        });

        resetBtn.addEventListener('click', function () {
          answered = 0;
          correct = 0;
          qEls.forEach(function (wrap, i) {
            wrap.removeAttribute('data-answered');
            Array.prototype.slice.call(wrap.querySelectorAll('.opt')).forEach(function (el) {
              el.disabled = false;
              el.removeAttribute('data-state');
            });
            Array.prototype.slice.call(wrap.querySelectorAll('.reveal')).forEach(function (d) { d.open = false; });
            document.getElementById('fb-' + i).innerHTML = '';
          });
          paintScore();
          quizListEl.scrollIntoView({ block: 'start' });
        });

        paintScore();
      }

      /* ── Apply it ─────────────────────────────────────────── */
      if (scenListEl && SCENARIOS.length) {
        scenListEl.innerHTML = SCENARIOS.map(function (s, i) {
          var hints = (s.hints || []).map(function (h, k) {
            return '<details class="reveal"><summary>Hint ' + (k + 1) + '</summary>' +
              '<div class="reveal-body"><p>' + esc(h) + '</p></div></details>';
          }).join('');

          var steps = (s.walkthrough || []).map(function (w) {
            return '<li>' + esc(w) + '</li>';
          }).join('');

          var checks = (s.checklist || []).map(function (c) {
            return '<li>' + esc(c) + '</li>';
          }).join('');

          return '<article class="scen">' +
            '<div class="quiz-head">' +
              '<span class="quiz-n">Scenario ' + (i + 1) + '</span>' +
              (s.topic ? '<span class="term-src">' + esc(s.topic) + '</span>' : '') +
            '</div>' +
            '<h3 class="scen-title">' + esc(s.title) + '</h3>' +
            '<p class="scen-setup">' + esc(s.setup) + '</p>' +
            '<p class="scen-task"><strong>Your task</strong>' + esc(s.task) + '</p>' +
            hints +
            '<details class="reveal reveal--work"><summary>Work it through</summary>' +
              '<div class="reveal-body">' +
                (steps ? '<ol class="steps">' + steps + '</ol>' : '') +
                (checks ? '<h5>A strong answer covers</h5><ul class="check">' + checks + '</ul>' : '') +
              '</div>' +
            '</details>' +
            '</article>';
        }).join('');
      }
    })();
  </script>
