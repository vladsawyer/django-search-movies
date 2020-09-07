function addComment(name, id) {
        document.getElementById("comment-parent").value = id;
        document.getElementById("contact-comment").innerText = `${name}, `
    }
