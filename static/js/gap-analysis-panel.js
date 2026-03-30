/**
 * Gap analysis UI: analyze, chart, PDF extract, AI tool injectors.
 * Requires resume-ai.js (ResumeAI). Used on ai_tools.html and resume / admissions templates.
 */
(function () {
  function animateGapChartOnCanvas(canvas, labelEl, score) {
    if (!canvas || !labelEl) return;
    var ctx = canvas.getContext('2d');
    var dpr = window.devicePixelRatio || 1;
    var size = 220;
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    canvas.style.width = size + 'px';
    canvas.style.height = size + 'px';
    ctx.scale(dpr, dpr);
    var cx = size / 2,
      cy = size / 2,
      radius = size / 2 - 12,
      lineWidth = 18;
    var startAngle = -Math.PI / 2,
      duration = 1200,
      startTime = null;
    var scoreColor = score >= 70 ? '#7FAF9D' : score >= 40 ? '#4FA3A5' : '#C8766A';
    var trackColor = 'rgba(31, 42, 68, 0.08)';
    function easeOutCubic(t) {
      return 1 - Math.pow(1 - t, 3);
    }
    function frame(timestamp) {
      if (!startTime) startTime = timestamp;
      var elapsed = timestamp - startTime;
      var progress = Math.min(elapsed / duration, 1);
      var eased = easeOutCubic(progress);
      var currentScore = Math.round(eased * score);
      var sweepAngle = (eased * score / 100) * Math.PI * 2;
      ctx.clearRect(0, 0, size, size);
      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, Math.PI * 2);
      ctx.strokeStyle = trackColor;
      ctx.lineWidth = lineWidth;
      ctx.lineCap = 'round';
      ctx.stroke();
      if (sweepAngle > 0.01) {
        ctx.beginPath();
        ctx.arc(cx, cy, radius, startAngle, startAngle + sweepAngle);
        ctx.strokeStyle = scoreColor;
        ctx.lineWidth = lineWidth;
        ctx.lineCap = 'round';
        ctx.stroke();
      }
      labelEl.textContent = currentScore + '%';
      if (progress < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function initGapAnalysisPanel() {
    var analyzeBtn = document.getElementById('gapAnalyzeBtn');
    var errorEl = document.getElementById('gapError');
    if (!analyzeBtn || !errorEl || typeof ResumeAI === 'undefined') return;

    analyzeBtn.addEventListener('click', function () {
      var resume = document.getElementById('gapResume').value.trim();
      var job = document.getElementById('gapJob').value.trim();
      if (!resume || !job) {
        errorEl.textContent = 'Please paste both your resume and the job description.';
        errorEl.style.display = 'block';
        return;
      }
      if (!ResumeAI.canUseAI()) {
        errorEl.textContent = 'Please save your API key first.';
        errorEl.style.display = 'block';
        return;
      }
      errorEl.style.display = 'none';
      analyzeBtn.disabled = true;
      analyzeBtn.innerHTML = '<span class="gap-btn-spinner"></span> Analyzing your resume...';
      document.getElementById('gapResults').style.display = 'none';

      ResumeAI.analyzeGap(resume, job)
        .then(function (data) {
          resumeTextForTools = resume;
          renderGapResults(data);
          document.getElementById('gapResults').style.display = 'block';
          injectAITools();
          document.getElementById('gapResults').scrollIntoView({ behavior: 'smooth', block: 'start' });
        })
        .catch(function (e) {
          errorEl.textContent = e.message || 'Something went wrong. Please try again.';
          errorEl.style.display = 'block';
        })
        .finally(function () {
          analyzeBtn.disabled = false;
          analyzeBtn.innerHTML = 'Analyze my resume <span class="btn-arrow" aria-hidden="true">→</span>';
        });
    });

    function renderGapResults(data) {
      document.getElementById('gapSummaryText').textContent = data.summary;
      var strengthsEl = document.getElementById('gapStrengths');
      if (data.strengths.length) {
        strengthsEl.innerHTML =
          '<h4 class="gap-strengths-title">What you\'re doing well</h4><ul class="gap-strengths-list">' +
          data.strengths
            .map(function (s) {
              return '<li>' + s + '</li>';
            })
            .join('') +
          '</ul>';
      } else {
        strengthsEl.innerHTML = '';
      }
      document.getElementById('gapKeywords').innerHTML = data.missing_keywords.map(function (kw) {
        return '<span class="gap-keyword-tag">' + kw + '</span>';
      }).join('');
      document.getElementById('gapSuggestions').innerHTML = data.suggestions.map(function (s) {
        return '<li>' + s + '</li>';
      }).join('');
      animateGapChartOnCanvas(
        document.getElementById('gapChart'),
        document.getElementById('gapScoreLabel'),
        data.match_score
      );
    }

    var resumeTextForTools = '';
    var pdfInput = document.getElementById('gapResumePdf');
    var resumeTextarea = document.getElementById('gapResume');
    var sourceLabel = document.getElementById('gapResumeSource');

    if (pdfInput) {
      pdfInput.addEventListener('change', function () {
        var file = this.files[0];
        if (!file) return;
        sourceLabel.textContent = 'Extracting text...';
        sourceLabel.style.color = 'var(--text-muted)';
        var formData = new FormData();
        formData.append('file', file);
        fetch('/resume/api/ai/extract-pdf/', {
          method: 'POST',
          body: formData,
          headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '' },
        })
          .then(function (r) {
            return r.json();
          })
          .then(function (data) {
            if (data.error) throw new Error(data.error);
            resumeTextarea.value = data.text;
            sourceLabel.textContent = file.name + ' ✓';
            sourceLabel.style.color = 'var(--sage)';
          })
          .catch(function (e) {
            sourceLabel.textContent = e.message || 'Failed to extract';
            sourceLabel.style.color = '#C8766A';
          })
          .finally(function () {
            pdfInput.value = '';
          });
      });
    }

    function injectAITools() {
      var bulletEl = document.getElementById('aiBulletTool');
      var summaryEl = document.getElementById('aiSummaryTool');
      var skillsEl = document.getElementById('aiSkillsTool');
      if (bulletEl && !bulletEl.hasChildNodes()) {
        bulletEl.appendChild(ResumeAI.createBulletEnhancer('your major'));
        summaryEl.appendChild(ResumeAI.createSummaryGenerator('your major'));
        skillsEl.appendChild(ResumeAI.createSkillsSuggester('your major'));
      }
    }

    ResumeAI.checkServer();
  }

  function initAdmissionsGapAnalysisPanel() {
    var analyzeBtn = document.getElementById('gapAnalyzeBtnAdmissions');
    var errorEl = document.getElementById('gapErrorAdmissions');
    if (!analyzeBtn || !errorEl || typeof ResumeAI === 'undefined') return;

    analyzeBtn.addEventListener('click', function () {
      var essay = document.getElementById('gapEssayDraft').value.trim();
      var promptText = document.getElementById('gapAdmissionsPrompt').value.trim();
      if (!essay || !promptText) {
        errorEl.textContent = 'Please paste both your essay draft and the admissions prompt.';
        errorEl.style.display = 'block';
        return;
      }
      if (!ResumeAI.canUseAI()) {
        errorEl.textContent = 'Please save your API key first.';
        errorEl.style.display = 'block';
        return;
      }
      errorEl.style.display = 'none';
      analyzeBtn.disabled = true;
      analyzeBtn.innerHTML = '<span class="gap-btn-spinner"></span> Analyzing your essay...';
      document.getElementById('gapResultsAdmissions').style.display = 'none';

      ResumeAI.analyzeGapAdmissions(essay, promptText)
        .then(function (data) {
          document.getElementById('gapSummaryTextAdmissions').textContent = data.summary;
          var strengthsEl = document.getElementById('gapStrengthsAdmissions');
          if (data.strengths.length) {
            strengthsEl.innerHTML =
              '<h4 class="gap-strengths-title">What you\'re doing well</h4><ul class="gap-strengths-list">' +
              data.strengths
                .map(function (s) {
                  return '<li>' + s + '</li>';
                })
                .join('') +
              '</ul>';
          } else {
            strengthsEl.innerHTML = '';
          }
          document.getElementById('gapKeywordsAdmissions').innerHTML = data.missing_keywords.map(function (kw) {
            return '<span class="gap-keyword-tag">' + kw + '</span>';
          }).join('');
          document.getElementById('gapSuggestionsAdmissions').innerHTML = data.suggestions.map(function (s) {
            return '<li>' + s + '</li>';
          }).join('');
          animateGapChartOnCanvas(
            document.getElementById('gapChartAdmissions'),
            document.getElementById('gapScoreLabelAdmissions'),
            data.match_score
          );
          document.getElementById('gapResultsAdmissions').style.display = 'block';
          document.getElementById('gapResultsAdmissions').scrollIntoView({ behavior: 'smooth', block: 'start' });
        })
        .catch(function (e) {
          errorEl.textContent = e.message || 'Something went wrong. Please try again.';
          errorEl.style.display = 'block';
        })
        .finally(function () {
          analyzeBtn.disabled = false;
          analyzeBtn.innerHTML = 'Analyze my essay <span class="btn-arrow" aria-hidden="true">→</span>';
        });
    });

    var pdfInput = document.getElementById('gapEssayPdf');
    var essayTextarea = document.getElementById('gapEssayDraft');
    var sourceLabel = document.getElementById('gapEssaySource');

    if (pdfInput && essayTextarea && sourceLabel) {
      pdfInput.addEventListener('change', function () {
        var file = this.files[0];
        if (!file) return;
        sourceLabel.textContent = 'Extracting text...';
        sourceLabel.style.color = 'var(--text-muted)';
        var formData = new FormData();
        formData.append('file', file);
        fetch('/resume/api/ai/extract-pdf/', {
          method: 'POST',
          body: formData,
          headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '' },
        })
          .then(function (r) {
            return r.json();
          })
          .then(function (data) {
            if (data.error) throw new Error(data.error);
            essayTextarea.value = data.text;
            sourceLabel.textContent = file.name + ' ✓';
            sourceLabel.style.color = 'var(--sage)';
          })
          .catch(function (e) {
            sourceLabel.textContent = e.message || 'Failed to extract';
            sourceLabel.style.color = '#C8766A';
          })
          .finally(function () {
            pdfInput.value = '';
          });
      });
    }

    ResumeAI.checkServer();
  }

  function initEmbeddedGapPanel() {
    var panel = document.getElementById('academicGapPanel');
    var openBtn = document.getElementById('gapAnalysisOpenBtn');
    if (!panel || !openBtn) return;

    openBtn.addEventListener('click', function () {
      panel.hidden = false;
      var ta = document.getElementById('gapResume');
      var ql = document.querySelector('#rpEditor .ql-editor');
      if (ta && ql && !ta.value.trim()) {
        ta.value = ql.innerText.trim();
      }
      panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  function initEmbeddedAdmissionsGapPanel() {
    var panel = document.getElementById('academicGapPanelAdmissions');
    var openBtn = document.getElementById('gapAnalysisOpenBtnAdmissions');
    if (!panel || !openBtn) return;

    openBtn.addEventListener('click', function () {
      panel.hidden = false;
      var ta = document.getElementById('gapEssayDraft');
      var ql = document.querySelector('#rpEditor .ql-editor');
      if (ta && ql && !ta.value.trim()) {
        ta.value = ql.innerText.trim();
      }
      panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  function run() {
    initGapAnalysisPanel();
    initAdmissionsGapAnalysisPanel();
    initEmbeddedGapPanel();
    initEmbeddedAdmissionsGapPanel();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
