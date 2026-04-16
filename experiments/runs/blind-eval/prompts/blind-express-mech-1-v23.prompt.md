# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-express-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 express@HEAD 141mod 116sym
? What matching and dispatch rules do the Express docs describe for route parameters, query strings, and route skipping?


-- TREE
examples/  (43 files)
  auth/  content-negotiation/  cookie-sessions/  cookies/  downloads/  ejs/  error/  error-pages/  hello-world/  markdown/  ...+15
lib/  (6 files)
test/  (91 files)
  acceptance/  support/
index.js

-- INDEX
examples/auth/index.js                          134L  authenticate, restrict
examples/content-negotiation/db.js                9L  
examples/content-negotiation/index.js            46L  format
examples/content-negotiation/users.js            19L  
examples/cookie-sessions/index.js                25L  
examples/cookies/index.js                        53L  
examples/downloads/index.js                      40L  
examples/ejs/index.js                            57L  
examples/error-pages/index.js                   103L  
examples/error/index.js                          53L  error
examples/hello-world/index.js                    15L  
examples/markdown/index.js                       44L  
examples/multi-router/controllers/api_v1.js      15L  
examples/multi-router/controllers/api_v2.js      15L  
examples/multi-router/index.js                   18L  
examples/mvc/controllers/main/index.js            5L  
examples/mvc/controllers/pet/index.js            31L  
examples/mvc/controllers/user-pet/index.js       22L  
examples/mvc/controllers/user/index.js           41L  
examples/mvc/db.js                               16L  
examples/mvc/index.js                            95L  
examples/mvc/lib/boot.js                         83L  
examples/online/index.js                         61L  list
examples/params/index.js                         74L  
examples/resource/index.js                       95L  
examples/route-map/index.js                      75L  
examples/route-middleware/index.js               90L  andRestrictTo, andRestrictToSelf, loadUser
examples/route-separation/index.js               55L  
examples/route-separation/post.js                13L  
examples/route-separation/site.js                 5L  
examples/route-separation/user.js                47L  
examples/search/index.js                         83L  initializeRedis
examples/search/public/client.js                 15L  
  ...and 108 more modules

-- SYM
count                               M examples/view-locals/index.js:41     function count
authenticate                        M examples/auth/index.js:56     function authenticate
restrict                            M examples/auth/index.js:74     function restrict
format                              M examples/content-negotiation/index.js:28     function format
error                               M examples/error/index.js:13     function error
list                                M examples/online/index.js:39     function list
andRestrictTo                       M examples/route-middleware/index.js:49     function andRestrictTo
andRestrictToSelf                   M examples/route-middleware/index.js:35     function andRestrictToSelf
loadUser                            M examples/route-middleware/index.js:24     function loadUser
initializeRedis                     M examples/search/index.js:28     async_function initializeRedis
GithubView                          M examples/view-constructor/github-view.js:22     function GithubView
count2                              M examples/view-locals/index.js:79     function count2
ferrets                             M examples/view-locals/index.js:14     function ferrets
users2                              M examples/view-locals/index.js:93     function users2
users                               M examples/view-locals/index.js:55     function users
User                                M examples/view-locals/user.js:4      function User
error                               M examples/web-service/index.js:10     function error
logerror                            M lib/application.js:614    function logerror
tryRender                           M lib/application.js:624    function tryRender
createApplication                   M lib/express.js:35     function createApplication
defineGetter                        M lib/request.js:521    function defineGetter
sendfile                            M lib/response.js:919    function sendfile
stringify                           M lib/response.js:1022   function stringify
acceptParams                        M lib/utils.js:88     function acceptParams
createETagGenerator                 M lib/utils.js:248    function createETagGenerator
parseExtendedQueryString            M lib/utils.js:266    function parseExtendedQueryString
View                                M lib/view.js:51     function View
tryStat                             M lib/view.js:196    function tryStat

-- FOCUS
parseExtendedQueryString (lib/utils.js:266-271)
  sig: parseExtendedQueryString(str)
  behavior: DELEGATE(qs.parse -> result)
  uses: qs.parse

andRestrictTo (examples/route-middleware/index.js:49-58)
  sig: andRestrictTo(role)
  behavior: DELEGATE(function -> result)
  uses: req.authenticatedUser.role

andRestrictToSelf (examples/route-middleware/index.js:35-48)
  sig: andRestrictToSelf(req, res, next)
  uses: req.authenticatedUser.id, req.user.id

createApplication (lib/express.js:35-56)
  uses: app.handle, EventEmitter.prototype, app.request, Object.create

loadUser (examples/route-middleware/index.js:24-34)
  sig: loadUser(req, res, next)
  uses: req.params.id, req.user

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 5 symbols in L3, 2 with behavior annotations
drill: lib/utils.js (~2 lines, parseExtendedQueryString)
drill: lib/express.js (~14 lines, createApplication)
drill: examples/route-middleware/index.js (~11 lines, andRestrictToSelf)
drill: examples/route-middleware/index.js (~5 lines, loadUser)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## parseExtendedQueryString  (lib/utils.js L266-271)
```

function parseExtendedQueryString(str) {
  return qs.parse(str, {
    allowPrototypes: true
  });
}
```

## loadUser  (examples/route-middleware/index.js L24-34)
```

function loadUser(req, res, next) {
  // You would fetch your user from the db
  var user = users[req.params.id];
  if (user) {
    req.user = user;
    next();
  } else {
    next(new Error('Failed to load user ' + req.params.id));
  }
}
```

## andRestrictToSelf  (examples/route-middleware/index.js L35-48)
```

function andRestrictToSelf(req, res, next) {
  // If our authenticated user is the user we are viewing
  // then everything is fine :)
  if (req.authenticatedUser.id === req.user.id) {
    next();
  } else {
    // You may want to implement specific exceptions
    // such as UnauthorizedError or similar so that you
    // can handle these can be special-cased in an error handler
    // (view ./examples/pages for this)
    next(new Error('Unauthorized'));
  }
}
```

## createApplication  (lib/express.js L35-56)
```

function createApplication() {
  var app = function(req, res, next) {
    app.handle(req, res, next);
  };

  mixin(app, EventEmitter.prototype, false);
  mixin(app, proto, false);

  // expose the prototype that will get set on requests
  app.request = Object.create(req, {
    app: { configurable: true, enumerable: true, writable: true, value: app }
  })

  // expose the prototype that will get set on responses
  app.response = Object.create(res, {
    app: { configurable: true, enumerable: true, writable: true, value: app }
  })

  app.init();
  return app;
}
```

## acceptParams  (lib/utils.js L88-120)
```

function acceptParams (str) {
  var length = str.length;
  var colonIndex = str.indexOf(';');
  var index = colonIndex === -1 ? length : colonIndex;
  var ret = { value: str.slice(0, index).trim(), quality: 1, params: {} };

  while (index < length) {
    var splitIndex = str.indexOf('=', index);
    if (splitIndex === -1) break;

    var colonIndex = str.indexOf(';', index);
    var endIndex = colonIndex === -1 ? length : colonIndex;

    if (splitIndex > endIndex) {
      index = str.lastIndexOf(';', splitIndex - 1) + 1;
      continue;
    }

    var key = str.slice(index, splitIndex).trim();
    var value = str.slice(splitIndex + 1, endIndex).trim();

    if (key === 'q') {
      ret.quality = parseFloat(value);
    } else {
      ret.params[key] = value;
    }

    index = endIndex + 1;
  }

  return ret;
}
```

## createETagGenerator  (lib/utils.js L248-257)
```

function createETagGenerator (options) {
  return function generateETag (body, encoding) {
    var buf = !Buffer.isBuffer(body)
      ? Buffer.from(body, encoding)
      : body

    return etag(buf, options)
  }
}
```

## andRestrictTo  (examples/route-middleware/index.js L49-58)
```

function andRestrictTo(role) {
  return function(req, res, next) {
    if (req.authenticatedUser.role === role) {
      next();
    } else {
      next(new Error('Unauthorized'));
    }
  }
}
```
--- END SOURCE SNIPPETS ---

QUESTION: What matching and dispatch rules do the Express docs describe for route parameters, query strings, and route skipping?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
