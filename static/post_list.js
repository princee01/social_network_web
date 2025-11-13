const csrftoken = getCookie("csrftoken");
    async function sendReaction(postId, reactionType) {
        try {
        const response = await fetch(`/${postId}/react/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrftoken,
          },
          body: new URLSearchParams({
            reaction_type: reactionType,
          }),
        });
        const data = await response.json();
        document.getElementById(`like-count-${postId}`).innerText =
          data.like_count;
        document.getElementById(`dislike-count-${postId}`).innerText =
          data.dislike_count;
      } catch (error) {
        console.error("Error:", error);
      }
    }

    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
          cookie = cookie.trim();
          if (cookie.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    async function deletePost(e, postId) {
      e.preventDefault();
      const response = await fetch(`/${postId}/delete/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
        },
      });
      if (response.ok) {
        document.getElementById(`post-${postId}`).remove();
      } else {
        alert("Failed to delete the post.");
      }
    }

async function editPost(e, postId) {
      e.preventDefault();
      const response = await fetch(`/${postId}/edit/`, {
        method: "GET",
        headers: {
          "X-CSRFToken": csrftoken,
        },
      });
      if (response.ok) {
        window.location.href = `/${postId}/edit/`;
      } else {
        alert("Failed to load edit page.");
      }
}