const navbar = document.querySelector('.navbar-feeds')
navbar.innerHTML = `<div class="navbar-feeds">
<nav class="navbar navbar-expand-lg gradient"
  style="background-color: #2067ea; position: fixed; top: 0; width: 100%;">
  <div class="container">
    <a class="navbar-brand h5" id="brand" href="/"><img src="../static/Personal/Images/display/logo.png"
        style="width: 40px; height: 40px; margin-top: -6px;"> &ThickSpace; Shelfmate</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
      aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-end" id="navbarNavDropdown">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/feed/features">Features</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/feed/faq">FAQs</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/feed/about">About Us</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
            aria-controls="offcanvasRight" href="" onmouseenter="if(window.location.href!=window.location.origin+'/'){window.location.replace('/');}">Sign Up</a>
        </li>
      </ul>
      </li>
      </ul>
    </div>
  </div>
</nav><br><br><br>
<div class="offcanvas offcanvas-end" data-bs-backdrop="static" tabindex="-1" id="offcanvasRight"
  aria-labelledby="offcanvasRightLabel" style="background-color:beige;">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasRightLabel"
      style="color:darkslategray; font-family:Verdana, Geneva, Tahoma, sans-serif; font-weight: 700;">SIGN UP</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <form class="row g-3" method="post" autocomplete="off">
      <div class="col-12">
        <label for="email-signup" class="form-label">Email</label>
        <input type="email" class="form-control" name="email-signup" placeholder="Your Email" required>
      </div>
      <div class="col-12">
        <label for="name-signup" class="form-label">Full Name</label>
        <input type="text" class="form-control" name="name-signup" placeholder="Your Name" required>
      </div>
      <div class="col-md-6">
        <label for="username-signup" class="form-label">Username</label>
        <input type="text" class="form-control" name="username-signup" placeholder="Create Username" required>
      </div>
      <div class="col-md-6">
        <label for="password-signup" class="form-label">Password</label>
        <input type="password" class="form-control" name="password-signup" placeholder="Create Password" required>
      </div>
      <div class="col-12">
        <label for="confirm-pass-signup" class="form-label">Confirm Password</label>
        <input type="password" class="form-control" name="confirm-pass-signup" placeholder="Retype Password" required>
      </div><br><hr>
      <div class="col-12 d-grid gap-2">
        <button type="submit" class="btn btn-success" name="sign-up" onclick="JavaScript:post_type('sign')">Sign Up</button>
      </div>
    </form><br><br>
    <a data-bs-toggle="offcanvas" data-bs-target="#staticBackdrop" aria-controls="staticBackdrop" href="" ,
      style="text-decoration: underline;">
      Already a member? <b>LOGIN</b>
    </a>
  </div>
</div>
<div class="offcanvas offcanvas-start" data-bs-backdrop="static" tabindex="-1" id="staticBackdrop"
  aria-labelledby="staticBackdropLabel" style="background-color:beige;">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasRightLabel"
      style="color:darkslategray; font-family:Verdana, Geneva, Tahoma, sans-serif; font-weight: 700;">LOG IN</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <form class="row g-3" method="post" autocomplete="off">
      <div class="col-12">
        <div class="col-12">
          <label for="username_email-login" class="form-label">Username</label>
          <input type="text" class="form-control" name="username_email-login" placeholder="Username or Email" required>
        </div><br><br>
        <label for="password-login" class="form-label">Password</label>
        <input type="password" class="form-control" name="password-login" placeholder="Your Password" required>
      </div><br><hr>
      <div class="col-12 d-grid gap-2">
        <button type="submit" class="btn btn-success" name="log-in" onclick="JavaScript:post_type('log')">Log In</button>
      </div>
    </form><br><br><br>

    <a data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight" href="" ,
      style="text-decoration: underline;">
      New to Shelfmate? <b>SIGNUP</b>
    </a>
  </div>
</div>`

const footer = document.querySelector('.footer-feeds')
footer.innerHTML = `</div>
<footer class="bd-footer py-4 py-md-5 mt-5 bg-body-tertiary">
  <div class="container py-4 py-md-5 px-4 px-md-3 text-body-secondary">
    <div class="row">
      <div class="col-lg-4 mb-3">
        <a class="d-inline-flex align-items-center mb-2 text-body-emphasis text-decoration-none" href="/"
          aria-label="Bootstrap">
          <img src="../static/Personal/Images/display/logo.png" width="30px">&ThickSpace;
          <span class="fs-5">Shelmate</span>
        </a>
        <ul class="list-unstyled small">
          <li class="mb-2">Designed and built with all the love in the world by the <a href="/feed/about">Shelmate
              team</a>.</li>
          <li class="mb-2"></li>
          <li class="mb-2">&copy; Currently v1.0.0-school.</li>
        </ul>
      </div>
      <div class="col-6 col-lg-4 offset-lg-1 mb-2">
        <h5>Links</h5>
        <ul class="list-unstyled">
          <li class="mb-2"><a class="style-a" href="/">Home</a></li>
          <li class="mb-2"><a class="style-a" href="/feed/faq">FAQs</a></li>
          <li class="mb-2"><a class="style-a" href="/feed/features">Features</a></li>
          <li class="mb-2"><a class="style-a" href="/feed/about">About Us</a></li>
          <li class="mb-2"><a class="style-a" href="/feed/how">How to use</a></li>
        </ul>
      </div>
      <div class="col-6 col-lg-3 mb-2">
        <h5>Creators</h5>
        <ul class="list-unstyled">
          <li class="mb-2"><a class="style-a" href="/feed/creators#c1">Sauhardya</a></li>
          <li class="mb-2"><a class="style-a" href="/feed/creators#c2">Sayan</a></li>
          <li class="mb-2"><a class="style-a" href="/feed/creators#c3">Arunaditya</a></li>
          <li class="mb-2"><a class="style-a" href="/feed/creators#c4">Shagnik S</a></li>
          <li class="mb-2"><a class="style-a" href="/feed/creators#c6">Swapnanil</a></li>
        </ul>
      </div>
      <div class="col-lg-4">
        <ul class="list-unstyled small" id="follow-apps">
          <a href="https://facebook.com" target="_blank"><img src="../static/Personal/Images/follow/facebook.png" width="30px"></a>
          <a href="https://quora.com" target="_blank"><img src="../static/Personal/Images/follow/quora.png" width="34px"></a>
          <a href="https://instagram.com" target="_blank"><img src="../static/Personal/Images/follow/instagram.png" width="31px"></a>
          <a href="https://youtube.com" target="_blank"><img src="../static/Personal/Images/follow/youtube.png" width="31px"></a>
        </ul>
      </div>
    </div>
  </div>
  </div>
</footer>`

function post_type(type) {
  document.cookie = "type=" + type
}