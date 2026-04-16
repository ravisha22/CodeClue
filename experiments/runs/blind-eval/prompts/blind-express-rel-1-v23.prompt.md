# Blind Evaluation Prompt - MRLF v2.4
# Task: blind-express-rel-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 express@HEAD 141mod 116sym
? What is the relationship between an Express app, mounted routers, and router-level middleware?


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
createApplication (lib/express.js:35-56)
  uses: app.handle, EventEmitter.prototype, app.request, Object.create

andRestrictTo (examples/route-middleware/index.js:49-58)
  sig: andRestrictTo(role)
  behavior: DELEGATE(function -> result)
  uses: req.authenticatedUser.role

andRestrictToSelf (examples/route-middleware/index.js:35-48)
  sig: andRestrictToSelf(req, res, next)
  uses: req.authenticatedUser.id, req.user.id

loadUser (examples/route-middleware/index.js:24-34)
  sig: loadUser(req, res, next)
  uses: req.params.id, req.user

-- GAPS
type: RELATIONAL (answerable from L2-L3 structure)
coverage: 4 symbols in L3, 1 with behavior annotations

--- CLUE FILE END ---

QUESTION: What is the relationship between an Express app, mounted routers, and router-level middleware?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
