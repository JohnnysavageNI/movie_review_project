document.addEventListener("DOMContentLoaded", () => {

  // DELETE comment 
  const deleteButtons = document.querySelectorAll(".btn-delete-comment");
  const deleteModalElement = document.getElementById("deleteModal");
  const deleteConfirm = document.getElementById("deleteConfirm");
  const deleteModal = deleteModalElement ? new bootstrap.Modal(deleteModalElement) : null;

  if (deleteModal && deleteConfirm) {
    deleteButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const commentId = button.getAttribute("data-comment-id");
        const movieId = window.location.pathname.split("/")[2];
        const deleteUrl = `/movies/${movieId}/delete_comment/${commentId}`;
        deleteConfirm.setAttribute("href", deleteUrl);
        deleteModal.show();
      });
    });
  }

  // EDIT comment
  const editButtons = document.querySelectorAll(".btn-edit-comment");
  const commentForm = document.getElementById("commentForm");
  const commentText = document.getElementById("id_content");
  const submitButton = document.getElementById("submitButton");

  editButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const commentId = button.getAttribute("data-comment-id");
      const commentContent = document.querySelector(`#comment${commentId} p`)?.innerText || "";
      const editUrl = button.getAttribute("data-url");

      if (commentForm && commentText) {
        commentText.value = commentContent;
        if (editUrl) commentForm.setAttribute("action", editUrl);
        if (submitButton) submitButton.innerText = "Update Comment";
      }
    });
  });
});