const code = `<div class="list-group list-group-flush mx-3 mt-4 container-fluid" style="cursor: pointer;">
<a href="/dashboard/account" class="list-group-item list-group-item-action py-2 ripple" id="account">
    <i class="fas fa-tachometer-alt fa-fw me-3"></i><span><img
            src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Main
        dashboard</span>
</a>
<a href="/dashboard/add-resource" class="list-group-item list-group-item-action py-2 ripple" id="add-resource">
    <i class="fas fa-chart-area fa-fw me-3"></i><span><img
            src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Add
        Resources</span>
</a>
<a href="/dashboard/all-resource" class="list-group-item list-group-item-action py-2 ripple" id="all-resource"><i
    class="fas fa-lock fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;All
    Resources</span></a>
<a href="/dashboard/borrow-request" class="list-group-item list-group-item-action py-2 ripple" id="borrow-request"><i
    class="fas fa-chart-line fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Borrow
    Request</span></a>
<a href="/dashboard/check-in" class="list-group-item list-group-item-action py-2 ripple" id="check-in">
<i class="fas fa-chart-pie fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Check-In
    User</span>
</a>
<a href="/dashboard/checked-user" class="list-group-item list-group-item-action py-2 ripple" id="checked-user"><i
    class="fas fa-chart-bar fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Checked-In
    Readers</span></a>
<a href="/dashboard/readers-history" class="list-group-item list-group-item-action py-2 ripple" id="readers-history"><i
    class="fas fa-globe fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Readers
    History</span></a>
<a href="/dashboard/add-member" class="list-group-item list-group-item-action py-2 ripple" id="add-member"><i
    class="fas fa-building fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Add
    Member</span></a>
<a href="/dashboard/all-member" class="list-group-item list-group-item-action py-2 ripple" id="all-member"><i
    class="fas fa-calendar fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;All
    Members</span></a>
<a href="/dashboard/borrow-history" class="list-group-item list-group-item-action py-2 ripple" id="borrow-history"><i
    class="fas fa-users fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Borrow History</span></a>
<a href="/dashboard/borrowed-data" class="list-group-item list-group-item-action py-2 ripple" id="borrowed-data"><i
    class="fas fa-money-bill fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Borrowed
    Resources</span></a>
<a href="/dashboard/library" class="list-group-item list-group-item-action py-2 ripple" id="library"><i
    class="fas fa-money-bill fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Library
    Details</span></a>
<a href="/dashboard/minor-settings" class="list-group-item list-group-item-action py-2 ripple" id="minor-settings"><i
    class="fas fa-money-bill fa-fw me-3"></i><span><img
        src="../static/Personal/Images/display/bullet.jpg" width="30px">&nbsp;&nbsp;Minor
    Settings</span></a>
<a class="list-group-item list-group-item-action py-2 ripple"><i
        class="fas fa-money-bill fa-fw me-3"></i></a>

</div>
`

function create_active(link) {
    const position = document.getElementsByClassName('dash-content')[0];
    position.innerHTML = code;
    var index = link.search('dashboard/')
    link = link.slice(index + 10)

    for (let i = 0; i < document.getElementsByClassName('ripple').length-1; i++) {
        const elem = document.getElementsByClassName('ripple')[i];
        if (elem.id == link) {
            elem.className += " active"
            elem.removeAttribute("href")
        }
        else {
            elem.addEventListener('click', (event) => {
                if (!event.ctrlKey) {
                    let main = document.getElementsByTagName('main')[0]
                    main.style.backgroundColor = "white";
                    main.innerHTML += `<div class="show" id="loading"><div id="loading-content">
                <div class="loader"></div>
                </div></div>`
                }
            })
        }
    }
}

create_active(window.location.href)