// htmx error pattern (design rule: errors inline, no toasts). When an htmx request fails,
// the target shows one `.err` line with a "Try again" hint instead of the content.
document.addEventListener("htmx:responseError", function (event) {
  var target = event.detail.target;
  if (!target) return;
  var message = document.createElement("p");
  message.className = "err";
  message.setAttribute("role", "alert");
  message.textContent = "Something went wrong. Try again.";
  target.replaceChildren(message);
});
