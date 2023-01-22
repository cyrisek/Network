document.addEventListener('DOMContentLoaded', function () {
    // Submit new post
    document.querySelector('#post').onsubmit = new_post;
    // Like or Unlike post
    document.querySelectorAll("i").forEach(e => {

        e.onclick = function () {

            like(this);
        }
    });
    // edit button
    document.querySelectorAll(".edit").forEach(e => {

        e.onclick = function () {

            edit(this);
        }
    });
});

// Send new Post
function new_post() {
    const post_body = document.querySelector('#post-body').value;

    fetch('/new_post', {
        method: 'POST',
        body: JSON.stringify({
            body: post_body,
        })
    })

        .then(response => response.json())
        .then(post => {

        });
    // reload page after sending post
    window.location.reload();
    return false;
}
// Like/ Unlike post
function like(element) {
    id = element.id
    fetch(`/like_post/${id}`, {
        method: 'POST',
    })
        .then(response => response.json())
        .then(response => {
            // Fill the heart
            if (response.liked) {
                document.getElementById(id).className = "bi bi-heart-fill";

            } else {
                document.getElementById(id).className = "bi bi-heart";
            }
            // update count
            document.getElementById(`likes-${id}`).innerHTML = response.count;

        });
}
// Edit Post
function edit(element, id) {
    id = element.id
    fetch(`/edit/${id}`)
        .then(response => response.json())
        .then(response => {
            // create New Elements
            let div = document.getElementById(`textarea-${id}`);
            let div2 = document.getElementById(`button-${id}`);
            let input = document.createElement("textarea");
            let save = document.createElement("button");
            save.setAttribute('onclick', `save_post(${id})`)
            save.id = `${id}`
            save.classList = "save btn btn-primary";
            save.innerHTML = "Save";
            input.name = "post";
            input.maxLength = "5000";
            input.cols = "150";
            input.rows = "8";
            input.classList = `new-text-${id}`;
            input.innerHTML = `${response.body}`;
            // Add elements to div's
            div.appendChild(input);
            div2.appendChild(save);
            // Delete old Elements
            let text = document.querySelector(`.text-${id}`);
            let editbtn = document.querySelector(`.edit-${id}`);
            text.remove();
            editbtn.remove();


        });
}
// Save Post
function save_post(id) {
    let text = document.querySelector(`.new-text-${id}`);
    body = text.value
    if (body === '') {
        return
    }
    text.remove()

    fetch(`/save/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            body: body,
        })
    })
        .then(response => response.json())
        .then(response => {
            // delete save button
            let save = document.querySelector(".save")
            save.remove()
            // create new elements
            let div = document.getElementById(`textarea-${id}`);
            let div2 = document.getElementById(`button-${id}`);
            let body = document.createElement("h4");
            let editbtn = document.createElement("a");
            body.classList = `card-title text-${id}`;
            body.id = "body";
            body.innerHTML = `${response.body}`;
            editbtn.setAttribute('onclick', "edit(this)")
            editbtn.classList = `edit edit-${id} btn btn-sm btn-primary text-white`;
            editbtn.id = `${id}`;
            editbtn.innerHTML = "Edit";
            // Add elements to div's
            div.appendChild(body);
            div2.appendChild(editbtn);
        })
}