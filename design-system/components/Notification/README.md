# Notification

A message from the system or an app, top right under the bar.

- Parts: symbol, bold title, up to three lines of text, time, optional actions in a footer.
- Normal messages leave after a few seconds. `data-urgency="critical"` gets a border and symbol in the accent and a draining line, and stays until dismissed.
- Enters from the right (`k-notif-in`), leaves to the right (`Kit.dismiss(el)`); the rest of the stack closes the gap.
- Title: what happened. Text: what it means or what to do. No exclamation marks.
