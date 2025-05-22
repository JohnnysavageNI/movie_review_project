document.addEventListener("DOMContentLoaded", () => {
  const editButtons = document.querySelectorAll(".btn-edit-comment");
  const deleteButtons = document.querySelectorAll(".btn-delete-comment");
  const commentText = document.getElementById("id_content");
  const commentForm = document.getElementById("commentForm");
  const submitButton = document.getElementById("submitButton");

  const deleteModalElement = document.getElementById("deleteModal");
  const deleteConfirm = document.getElementById("deleteConfirm");
  const deleteModal = deleteModalElement ? new bootstrap.Modal(deleteModalElement) : null;

  // Edit comment
 editButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const commentId = button.getAttribute("data-comment-id");
    const commentContentElement = document.querySelector(`#comment${commentId} p`);
    const commentContent = commentContentElement ? commentContentElement.innerText : "";

    if (commentText && commentForm) {
      commentText.value = commentContent;

      const formActionUrl = button.getAttribute("data-url");
      if (formActionUrl) {
        commentForm.setAttribute("action", formActionUrl);
      }

      if (submitButton) {
        submitButton.innerText = "Update Comment";
      }
    }
  });
});

  // Delete comment
  deleteButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const commentId = button.getAttribute("data-comment-id");
      const movieId = window.location.pathname.split("/")[2];
      const deleteUrl = `/movies/${movieId}/delete_comment/${commentId}`;
      if (deleteConfirm && deleteModal) {
        deleteConfirm.href = deleteUrl;
        deleteModal.show();
      }
    });
  });
});