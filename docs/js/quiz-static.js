/**
 * Static quiz logic for GitHub Pages. Loads quiz-data.json and provides scoring.
 */
(function() {
  var QUIZ_DATA = null;

  function loadData() {
    if (QUIZ_DATA) return Promise.resolve(QUIZ_DATA);
    return fetch('js/quiz-data.json').then(function(r) {
      if (!r.ok) throw new Error('Failed to load quiz data');
      return r.json();
    }).then(function(d) {
      QUIZ_DATA = d;
      return d;
    }).catch(function(e) {
      console.error('Quiz data load error:', e);
      return null;
    });
  }

  function getQuestions(short) {
    return loadData().then(function(d) {
      return short ? d.shortQuestions : d.fullQuestions;
    });
  }

  function getMajors() {
    return loadData().then(function(d) { return d.majors; });
  }

  function getMajorByKey(key) {
    return loadData().then(function(d) {
      for (var i = 0; i < d.majors.length; i++) {
        var m = d.majors[i];
        if (m.key === key) return { key: m.key, label: m.label, description: m.desc };
      }
      return null;
    });
  }

  function scoreQuiz(selectedOptions, data) {
    data = data || QUIZ_DATA;
    if (!data) throw new Error('Quiz data not loaded');
    var scores = {};
    data.fullQuestions.forEach(function(q) {
      q.options.forEach(function(opt) {
        if (selectedOptions.indexOf(opt.key) !== -1) {
          opt.categories.forEach(function(cat) {
            scores[cat] = (scores[cat] || 0) + 1;
          });
        }
      });
    });
    return Object.keys(scores).map(function(c) { return [c, scores[c]]; })
      .sort(function(a, b) { return b[1] - a[1]; });
  }

  function getCareersForMajor(majorKey, data) {
    data = data || QUIZ_DATA;
    var result = [], seen = {};
    data.careers.forEach(function(c) {
      if (c.majors.indexOf(majorKey) !== -1 && !seen[c.title]) {
        seen[c.title] = true;
        result.push({ title: c.title, description: c.description, category: c.category });
      }
    });
    return result;
  }

  function getTopCareers(scoreTuples, majorKey, maxCareers, data) {
    maxCareers = maxCareers || 12;
    data = data || QUIZ_DATA;
    var pool;
    if (majorKey) {
      pool = getCareersForMajor(majorKey, data);
    } else {
      var seen = {};
      pool = data.careers.filter(function(c) {
        if (seen[c.title]) return false;
        seen[c.title] = true;
        return true;
      }).map(function(c) { return { title: c.title, description: c.description, category: c.category }; });
    }
    var catScores = {};
    scoreTuples.forEach(function(t) { catScores[t[0]] = t[1]; });
    function careerScore(c) { return catScores[c.category] || 0; }
    pool.sort(function(a, b) { return careerScore(b) - careerScore(a); });
    return pool.slice(0, maxCareers).map(function(c, i) {
      var entry = Object.assign({}, c);
      entry.learn_more = data.careerLearnMore[c.title] || data.careerLearnMoreDefault;
      entry.compatibility_rank = i + 1;
      entry.match_score = careerScore(c);
      return entry;
    });
  }

  function getCategoryNames(data) {
    data = data || QUIZ_DATA;
    var map = {};
    data.categories.forEach(function(c) { map[c.key] = { name: c.name, desc: c.desc }; });
    return map;
  }

  function buildScoresWithNames(scoreTuples, data) {
    data = data || QUIZ_DATA;
    var names = getCategoryNames(data);
    return scoreTuples.map(function(t) {
      var info = names[t[0]] || { name: t[0], desc: '' };
      return [t[0], t[1], info.name, info.desc];
    });
  }

  function getResultsSummary(scoresWithNames, suggestions, majorLabel) {
    if (!scoresWithNames.length || !suggestions.length) return null;
    var topCats = scoresWithNames.slice(0, 3).map(function(s) { return s[2]; });
    var topCatStr = topCats.length > 1 ? topCats.slice(0, -1).join(', ') + ' and ' + topCats[topCats.length - 1] : topCats[0];
    var firstJobs = suggestions.slice(0, 3).map(function(s) { return s.title; });
    var firstJobsStr = firstJobs.length > 1 ? firstJobs.slice(0, -1).join(', ') + ', and ' + firstJobs[firstJobs.length - 1] : firstJobs[0];
    var intro = 'Your quiz results show strong alignment with ' + topCatStr + '. ';
    var jobsSentence = 'Roles like ' + firstJobsStr + ' appear at the top because they match these strengths most closely. ';
    var orderSentence = majorLabel
      ? 'All suggestions fit your ' + majorLabel + ' background and are ordered from most to least compatible with your personality. '
      : 'Suggestions are ordered from most to least compatible with your personality and interests. ';
    return intro + jobsSentence + orderSentence;
  }

  function getSuggestedMajors(scoreTuples, topN, data) {
    topN = topN || 6;
    data = data || QUIZ_DATA;
    var catScores = {};
    scoreTuples.forEach(function(t) { catScores[t[0]] = t[1]; });
    var majorTotals = {};
    data.careers.forEach(function(c) {
      var sc = catScores[c.category] || 0;
      c.majors.forEach(function(m) {
        majorTotals[m] = (majorTotals[m] || 0) + sc;
      });
    });
    var sorted = Object.keys(majorTotals).sort(function(a, b) { return majorTotals[b] - majorTotals[a]; });
    return sorted.slice(0, topN).map(function(key) {
      var m = data.majors.find(function(x) { return x.key === key; });
      return m ? [key, m.label, m.desc, majorTotals[key]] : null;
    }).filter(Boolean);
  }

  function getExploreSummary(scoresWithNames, suggestedMajors) {
    if (!scoresWithNames.length || !suggestedMajors.length) return null;
    var topCats = scoresWithNames.slice(0, 3).map(function(s) { return s[2]; });
    var topCatStr = topCats.length > 1 ? topCats.slice(0, -1).join(', ') + ' and ' + topCats[topCats.length - 1] : topCats[0];
    var majorNames = suggestedMajors.slice(0, 3).map(function(m) { return m[1]; });
    var majorStr = majorNames.length > 1 ? majorNames.slice(0, -1).join(', ') + ', and ' + majorNames[majorNames.length - 1] : majorNames[0];
    return 'Your answers show strong alignment with ' + topCatStr + '. ' +
      'That\'s why we\'re suggesting majors like ' + majorStr + '—they lead to careers that often match these strengths. ' +
      'You can explore jobs in any suggested major, or take the full quiz again after picking one to see roles tailored to that degree.';
  }

  window.QuizStatic = {
    loadData: loadData,
    getQuestions: getQuestions,
    getMajors: getMajors,
    getMajorByKey: getMajorByKey,
    scoreQuiz: scoreQuiz,
    getTopCareers: getTopCareers,
    getCategoryNames: getCategoryNames,
    buildScoresWithNames: buildScoresWithNames,
    getResultsSummary: getResultsSummary,
    getSuggestedMajors: getSuggestedMajors,
    getExploreSummary: getExploreSummary,
  };
})();
