
const editButtons = document.getElementsByClassName("btn-edit");
const commentText = document.getElementById("id_body");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");


    for (let button of editButtons) {
        button.addEventListener("click", (e) => {
            let commentId = e.target.getAttribute("data-comment_id");
            let commentContent = document.getElementById(`comment${commentId}`).innerText;
            console.log("id:", commentId);
            commentText.value = commentContent;
            submitButton.innerText = "Update";
            commentForm.setAttribute("action", `edit_comment/${commentId}`);
        });
    }

    for (let button of deleteButtons) {
        button.addEventListener("click", (e) => {
            const commentId = e.target.getAttribute("data-comment_id");
            const activitySlug = e.target.getAttribute("data-activity_slug");
            deleteConfirm.href = `/${activitySlug}/delete_comment/${commentId}`;
            deleteModal.show();
        });
    }