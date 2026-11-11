/* @ds-bundle: {"format": 4, "namespace": "Kit", "components": [{"name": "Button"}, {"name": "IconButton"}, {"name": "TextField"}, {"name": "SearchField"}, {"name": "Switch"}, {"name": "Checkbox"}, {"name": "Radio"}, {"name": "Segmented"}, {"name": "Slider"}, {"name": "Progress"}, {"name": "Ring"}, {"name": "Badge"}, {"name": "Tooltip"}, {"name": "Notification"}, {"name": "Osd"}, {"name": "Dialog"}, {"name": "List"}, {"name": "SettingRow"}, {"name": "InfoBlock"}, {"name": "Card"}, {"name": "Calendar"}, {"name": "ContextMenu"}, {"name": "Search"}, {"name": "TopBar"}, {"name": "EdgeDock"}, {"name": "MediaPlayer"}, {"name": "Visualizer"}, {"name": "SlantCard"}, {"name": "WindowFrame"}]} */
(function () {
  'use strict';
  var ICONS = {"search": "<path d=\"m21 21-4.34-4.34\" /> <circle cx=\"11\" cy=\"11\" r=\"8\" />", "cpu": "<path d=\"M12 20v2\" /> <path d=\"M12 2v2\" /> <path d=\"M17 20v2\" /> <path d=\"M17 2v2\" /> <path d=\"M2 12h2\" /> <path d=\"M2 17h2\" /> <path d=\"M2 7h2\" /> <path d=\"M20 12h2\" /> <path d=\"M20 17h2\" /> <path d=\"M20 7h2\" /> <path d=\"M7 20v2\" /> <path d=\"M7 2v2\" /> <rect x=\"4\" y=\"4\" width=\"16\" height=\"16\" rx=\"2\" /> <rect x=\"8\" y=\"8\" width=\"8\" height=\"8\" rx=\"1\" />", "memory-stick": "<path d=\"M12 12v-2\" /> <path d=\"M12 18v-2\" /> <path d=\"M16 12v-2\" /> <path d=\"M16 18v-2\" /> <path d=\"M2 11h1.5\" /> <path d=\"M20 18v-2\" /> <path d=\"M20.5 11H22\" /> <path d=\"M4 18v-2\" /> <path d=\"M8 12v-2\" /> <path d=\"M8 18v-2\" /> <rect x=\"2\" y=\"6\" width=\"20\" height=\"10\" rx=\"2\" />", "thermometer": "<path d=\"M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z\" />", "music": "<path d=\"M21 16V3a1 1 0 0 0-1.28-.96l-10 2.917a1 1 0 0 0-.72.96V19\" /> <circle cx=\"18\" cy=\"16\" r=\"3\" /> <circle cx=\"6\" cy=\"19\" r=\"3\" />", "bell": "<path d=\"M10.268 21a2 2 0 0 0 3.464 0\" /> <path d=\"M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326\" />", "power": "<path d=\"M12 2v10\" /> <path d=\"M18.4 6.6a9 9 0 1 1-12.77.04\" />", "video": "<path d=\"m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5\" /> <rect x=\"2\" y=\"6\" width=\"14\" height=\"12\" rx=\"2\" />", "settings": "<path d=\"M9.671 4.136a2.34 2.34 0 0 1 4.659 0 2.34 2.34 0 0 0 3.319 1.915 2.34 2.34 0 0 1 2.33 4.033 2.34 2.34 0 0 0 0 3.831 2.34 2.34 0 0 1-2.33 4.033 2.34 2.34 0 0 0-3.319 1.915 2.34 2.34 0 0 1-4.659 0 2.34 2.34 0 0 0-3.32-1.915 2.34 2.34 0 0 1-2.33-4.033 2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915\" /> <circle cx=\"12\" cy=\"12\" r=\"3\" />", "wifi": "<path d=\"M12 20h.01\" /> <path d=\"M2 8.82a15 15 0 0 1 20 0\" /> <path d=\"M5 12.859a10 10 0 0 1 14 0\" /> <path d=\"M8.5 16.429a5 5 0 0 1 7 0\" />", "bluetooth": "<path d=\"m7 7 10 10-5 5V2l5 5L7 17\" />", "volume-2": "<path d=\"M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z\" /> <path d=\"M16 9a5 5 0 0 1 0 6\" /> <path d=\"M19.364 18.364a9 9 0 0 0 0-12.728\" />", "sun": "<circle cx=\"12\" cy=\"12\" r=\"4\" /> <path d=\"M12 2v2\" /> <path d=\"M12 20v2\" /> <path d=\"m4.93 4.93 1.41 1.41\" /> <path d=\"m17.66 17.66 1.41 1.41\" /> <path d=\"M2 12h2\" /> <path d=\"M20 12h2\" /> <path d=\"m6.34 17.66-1.41 1.41\" /> <path d=\"m19.07 4.93-1.41 1.41\" />", "cloud": "<path d=\"M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z\" />", "chevron-left": "<path d=\"m15 18-6-6 6-6\" />", "chevron-right": "<path d=\"m9 18 6-6-6-6\" />", "x": "<path d=\"M18 6 6 18\" /> <path d=\"m6 6 12 12\" />", "minus": "<path d=\"M5 12h14\" />", "square": "<rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\" />", "check": "<path d=\"M20 6 9 17l-5-5\" />", "lock": "<rect width=\"18\" height=\"11\" x=\"3\" y=\"11\" rx=\"2\" ry=\"2\" /> <path d=\"M7 11V7a5 5 0 0 1 10 0v4\" />", "log-out": "<path d=\"m16 17 5-5-5-5\" /> <path d=\"M21 12H9\" /> <path d=\"M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4\" />", "moon": "<path d=\"M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401\" />", "rotate-cw": "<path d=\"M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8\" /> <path d=\"M21 3v5h-5\" />", "play": "<path d=\"M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z\" />", "pause": "<rect x=\"14\" y=\"3\" width=\"5\" height=\"18\" rx=\"1\" /> <rect x=\"5\" y=\"3\" width=\"5\" height=\"18\" rx=\"1\" />", "skip-back": "<path d=\"M17.971 4.285A2 2 0 0 1 21 6v12a2 2 0 0 1-3.029 1.715l-9.997-5.998a2 2 0 0 1-.003-3.432z\" /> <path d=\"M3 20V4\" />", "skip-forward": "<path d=\"M21 4v16\" /> <path d=\"M6.029 4.285A2 2 0 0 0 3 6v12a2 2 0 0 0 3.029 1.715l9.997-5.998a2 2 0 0 0 .003-3.432z\" />", "layout-grid": "<rect width=\"7\" height=\"7\" x=\"3\" y=\"3\" rx=\"1\" /> <rect width=\"7\" height=\"7\" x=\"14\" y=\"3\" rx=\"1\" /> <rect width=\"7\" height=\"7\" x=\"14\" y=\"14\" rx=\"1\" /> <rect width=\"7\" height=\"7\" x=\"3\" y=\"14\" rx=\"1\" />", "hard-drive": "<path d=\"M10 16h.01\" /> <path d=\"M2.212 11.577a2 2 0 0 0-.212.896V18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5.527a2 2 0 0 0-.212-.896L18.55 5.11A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z\" /> <path d=\"M21.946 12.013H2.054\" /> <path d=\"M6 16h.01\" />", "download": "<path d=\"M12 15V3\" /> <path d=\"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4\" /> <path d=\"m7 10 5 5 5-5\" />", "trash-2": "<path d=\"M10 11v6\" /> <path d=\"M14 11v6\" /> <path d=\"M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6\" /> <path d=\"M3 6h18\" /> <path d=\"M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2\" />", "copy": "<rect width=\"14\" height=\"14\" x=\"8\" y=\"8\" rx=\"2\" ry=\"2\" /> <path d=\"M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2\" />", "clipboard": "<rect width=\"8\" height=\"4\" x=\"8\" y=\"2\" rx=\"1\" ry=\"1\" /> <path d=\"M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2\" />", "folder": "<path d=\"M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z\" />", "file": "<path d=\"M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z\" /> <path d=\"M14 2v5a1 1 0 0 0 1 1h5\" />", "terminal": "<path d=\"M12 19h8\" /> <path d=\"m4 17 6-6-6-6\" />", "info": "<circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"M12 16v-4\" /> <path d=\"M12 8h.01\" />", "triangle-alert": "<path d=\"m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3\" /> <path d=\"M12 9v4\" /> <path d=\"M12 17h.01\" />", "usb": "<circle cx=\"10\" cy=\"7\" r=\"1\" /> <circle cx=\"4\" cy=\"20\" r=\"1\" /> <path d=\"M4.7 19.3 19 5\" /> <path d=\"m21 3-3 1 2 2Z\" /> <path d=\"M9.26 7.68 5 12l2 5\" /> <path d=\"m10 14 5 2 3.5-3.5\" /> <path d=\"m18 12 1-1 1 1-1 1Z\" />", "package": "<path d=\"M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z\" /> <path d=\"M12 22V12\" /> <polyline points=\"3.29 7 12 12 20.71 7\" /> <path d=\"m7.5 4.27 9 5.15\" />", "image": "<rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\" ry=\"2\" /> <circle cx=\"9\" cy=\"9\" r=\"2\" /> <path d=\"m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21\" />", "calendar": "<path d=\"M8 2v3\" /> <path d=\"M16 2v3\" /> <rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\" /> <path d=\"M3 9h18\" />", "monitor": "<rect width=\"20\" height=\"14\" x=\"2\" y=\"3\" rx=\"2\" /> <line x1=\"8\" x2=\"16\" y1=\"21\" y2=\"21\" /> <line x1=\"12\" x2=\"12\" y1=\"17\" y2=\"21\" />", "plus": "<path d=\"M5 12h14\" /> <path d=\"M12 5v14\" />", "arrow-right": "<path d=\"M5 12h14\" /> <path d=\"m12 5 7 7-7 7\" />", "eye": "<path d=\"M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0\" /> <circle cx=\"12\" cy=\"12\" r=\"3\" />", "eye-off": "<path d=\"M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49\" /> <path d=\"M14.084 14.158a3 3 0 0 1-4.242-4.242\" /> <path d=\"M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143\" /> <path d=\"m2 2 20 20\" />", "refresh-cw": "<path d=\"M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8\" /> <path d=\"M21 3v5h-5\" /> <path d=\"M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16\" /> <path d=\"M8 16H3v5\" />", "palette": "<path d=\"M12 22a1 1 0 0 1 0-20 10 9 0 0 1 10 9 5 5 0 0 1-5 5h-2.25a1.75 1.75 0 0 0-1.4 2.8l.3.4a1.75 1.75 0 0 1-1.4 2.8z\" /> <circle cx=\"13.5\" cy=\"6.5\" r=\".5\" fill=\"currentColor\" /> <circle cx=\"17.5\" cy=\"10.5\" r=\".5\" fill=\"currentColor\" /> <circle cx=\"6.5\" cy=\"12.5\" r=\".5\" fill=\"currentColor\" /> <circle cx=\"8.5\" cy=\"7.5\" r=\".5\" fill=\"currentColor\" />", "camera": "<path d=\"M13.997 4a2 2 0 0 1 1.76 1.05l.486.9A2 2 0 0 0 18.003 7H20a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h1.997a2 2 0 0 0 1.759-1.048l.489-.904A2 2 0 0 1 10.004 4z\" /> <circle cx=\"12\" cy=\"13\" r=\"3\" />", "crop": "<path d=\"M6 2v14a2 2 0 0 0 2 2h14\" /> <path d=\"M18 22V8a2 2 0 0 0-2-2H2\" />", "app-window": "<rect x=\"2\" y=\"4\" width=\"20\" height=\"16\" rx=\"2\" /> <path d=\"M10 4v4\" /> <path d=\"M2 8h20\" /> <path d=\"M6 4v4\" />", "keyboard": "<path d=\"M10 8h.01\" /> <path d=\"M12 12h.01\" /> <path d=\"M14 8h.01\" /> <path d=\"M16 12h.01\" /> <path d=\"M18 8h.01\" /> <path d=\"M6 8h.01\" /> <path d=\"M7 16h10\" /> <path d=\"M8 12h.01\" /> <rect width=\"20\" height=\"16\" x=\"2\" y=\"4\" rx=\"2\" />", "gauge": "<path d=\"m12 14 4-4\" /> <path d=\"M3.34 19a10 10 0 1 1 17.32 0\" />", "disc-3": "<circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"M6 12c0-1.7.7-3.2 1.8-4.2\" /> <circle cx=\"12\" cy=\"12\" r=\"2\" /> <path d=\"M18 12c0 1.7-.7 3.2-1.8 4.2\" />", "circle-alert": "<circle cx=\"12\" cy=\"12\" r=\"10\" /> <line x1=\"12\" x2=\"12\" y1=\"8\" y2=\"12\" /> <line x1=\"12\" x2=\"12.01\" y1=\"16\" y2=\"16\" />", "cloud-sun": "<path d=\"M12 2v2\" /> <path d=\"m4.93 4.93 1.41 1.41\" /> <path d=\"M20 12h2\" /> <path d=\"m19.07 4.93-1.41 1.41\" /> <path d=\"M15.947 12.65a4 4 0 0 0-5.925-4.128\" /> <path d=\"M13 22H7a5 5 0 1 1 4.9-6H13a3 3 0 0 1 0 6Z\" />", "sliders-horizontal": "<path d=\"M10 5H3\" /> <path d=\"M12 19H3\" /> <path d=\"M14 3v4\" /> <path d=\"M16 17v4\" /> <path d=\"M21 12h-9\" /> <path d=\"M21 19h-5\" /> <path d=\"M21 5h-7\" /> <path d=\"M8 10v4\" /> <path d=\"M8 12H3\" />", "zap": "<path d=\"M15.914 4a1.5 1.5 0 00-2.474-1.561l-9 9A1.5 1.5 0 005.5 14h4.002a.5.5 0 01.471.666L8.086 20a1.5 1.5 0 002.475 1.56l9-9A1.5 1.5 0 0018.5 10h-3.997a.5.5 0 01-.472-.667z\" />", "corner-down-left": "<path d=\"M20 4v7a4 4 0 0 1-4 4H4\" /> <path d=\"m9 10-5 5 5 5\" />", "arrow-up": "<path d=\"m5 12 7-7 7 7\" /> <path d=\"M12 19V5\" />", "book-open": "<path d=\"M12 5v16\" /> <path d=\"M20.001 19A2 2 0 0022 17V5a2 2 0 00-1.999-2L16 3.002A5 5 0 0012 5a5 5 0 00-4-2H4a2 2 0 00-2 2v12a2 2 0 001.999 2H8a5 5 0 014 2 5 5 0 014-2z\" />", "pipette": "<path d=\"m12 9-8.414 8.414A2 2 0 0 0 3 18.828v1.344a2 2 0 0 1-.586 1.414A2 2 0 0 1 3.828 21h1.344a2 2 0 0 0 1.414-.586L15 12\" /> <path d=\"m18 9 .4.4a1 1 0 1 1-3 3l-3.8-3.8a1 1 0 1 1 3-3l.4.4 3.4-3.4a1 1 0 1 1 3 3z\" /> <path d=\"m2 22 .414-.414\" />", "scan-line": "<path d=\"M3 7V5a2 2 0 0 1 2-2h2\" /> <path d=\"M17 3h2a2 2 0 0 1 2 2v2\" /> <path d=\"M21 17v2a2 2 0 0 1-2 2h-2\" /> <path d=\"M7 21H5a2 2 0 0 1-2-2v-2\" /> <path d=\"M7 12h10\" />", "history": "<path d=\"M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8\" /> <path d=\"M3 3v5h5\" /> <path d=\"M12 7v5l4 2\" />", "square-terminal": "<path d=\"m7 11 2-2-2-2\" /> <path d=\"M11 13h4\" /> <rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\" ry=\"2\" />", "wallpaper": "<path d=\"M12 17v4\" /> <path d=\"M8 21h8\" /> <path d=\"m9 17 6.1-6.1a2 2 0 0 1 2.81.01L22 15\" /> <circle cx=\"8\" cy=\"9\" r=\"2\" /> <rect x=\"2\" y=\"3\" width=\"20\" height=\"14\" rx=\"2\" />", "swatch-book": "<path d=\"M11 17a4 4 0 0 1-8 0V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2Z\" /> <path d=\"M16.7 13H19a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H7\" /> <path d=\"M 7 17h.01\" /> <path d=\"m11 8 2.3-2.3a2.4 2.4 0 0 1 3.404.004L18.6 7.6a2.4 2.4 0 0 1 .026 3.434L9.9 19.8\" />", "type": "<path d=\"M12 4v16\" /> <path d=\"M4 7V5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2\" /> <path d=\"M9 20h6\" />", "moon-star": "<path d=\"M18 5h4\" /> <path d=\"M20 3v4\" /> <path d=\"M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401\" />", "scan": "<path d=\"M3 7V5a2 2 0 0 1 2-2h2\" /> <path d=\"M17 3h2a2 2 0 0 1 2 2v2\" /> <path d=\"M21 17v2a2 2 0 0 1-2 2h-2\" /> <path d=\"M7 21H5a2 2 0 0 1-2-2v-2\" />", "clock": "<circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"M12 6v6l4 2\" />", "hard-drive-download": "<path d=\"M12 2v8\" /> <path d=\"m16 6-4 4-4-4\" /> <rect width=\"20\" height=\"8\" x=\"2\" y=\"14\" rx=\"2\" /> <path d=\"M6 18h.01\" /> <path d=\"M10 18h.01\" />", "images": "<path d=\"m22 11-1.296-1.296a2.4 2.4 0 0 0-3.408 0L11 16\" /> <path d=\"M4 8a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2\" /> <circle cx=\"13\" cy=\"7\" r=\"1\" fill=\"currentColor\" /> <rect x=\"8\" y=\"2\" width=\"14\" height=\"14\" rx=\"2\" />", "pencil": "<path d=\"M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z\" /> <path d=\"m15 5 4 4\" />", "undo-2": "<path d=\"M9 14 4 9l5-5\" /> <path d=\"M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5a5.5 5.5 0 0 1-5.5 5.5H11\" />", "command": "<path d=\"M15 6v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 0-3 3h12a3 3 0 1 0-3-3\" />"};
  var WALL = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 2560 1440\" preserveAspectRatio=\"xMidYMid slice\"><rect width=\"2560\" height=\"1440\" style=\"fill:var(--background)\"/><circle cx=\"1560\" cy=\"660\" r=\"250\" style=\"fill:var(--accent)\"/><circle cx=\"1560\" cy=\"1010\" r=\"430\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.55\"/><circle cx=\"1560\" cy=\"1010\" r=\"640\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.5\"/><circle cx=\"1560\" cy=\"1010\" r=\"900\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.42\"/><circle cx=\"1560\" cy=\"1010\" r=\"1210\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.34\"/><circle cx=\"1560\" cy=\"1010\" r=\"1560\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.26\"/><circle cx=\"1560\" cy=\"1010\" r=\"664\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.5\"/><path d=\"M2184.0 1010.0L2224.0 1010.0M2199.6 1032.3L2223.6 1033.2M2198.4 1054.6L2222.4 1056.3M2196.5 1076.9L2220.4 1079.4M2193.8 1099.1L2217.5 1102.4M2174.5 1118.4L2213.9 1125.3M2186.0 1143.1L2209.5 1148.1M2181.0 1164.8L2204.3 1170.6M2175.2 1186.4L2198.3 1193.0M2168.7 1207.8L2191.5 1215.2M2146.4 1223.4L2184.0 1237.1M2153.4 1249.7L2175.7 1258.7M2144.7 1270.3L2166.6 1280.1M2135.2 1290.6L2156.8 1301.1M2125.1 1310.5L2146.3 1321.7M2100.4 1322.0L2135.0 1342.0M2102.8 1349.1L2123.1 1361.9M2090.6 1367.9L2110.5 1381.3M2077.8 1386.2L2097.2 1400.3M2064.3 1404.0L2083.2 1418.8M2038.0 1411.1L2068.7 1436.8M2035.6 1438.2L2053.4 1454.3M2020.4 1454.6L2037.6 1471.3M2004.6 1470.4L2021.3 1487.6M1988.2 1485.6L2004.3 1503.4M1961.1 1488.0L1986.8 1518.7M1954.0 1514.3L1968.8 1533.2M1936.2 1527.8L1950.3 1547.2M1917.9 1540.6L1931.3 1560.5M1899.1 1552.8L1911.9 1573.1M1872.0 1550.4L1892.0 1585.0M1860.5 1575.1L1871.7 1596.3M1840.6 1585.2L1851.1 1606.8M1820.3 1594.7L1830.1 1616.6M1799.7 1603.4L1808.7 1625.7M1773.4 1596.4L1787.1 1634.0M1757.8 1618.7L1765.2 1641.5M1736.4 1625.2L1743.0 1648.3M1714.8 1631.0L1720.6 1654.3M1693.1 1636.0L1698.1 1659.5M1668.4 1624.5L1675.3 1663.9M1649.1 1643.8L1652.4 1667.5M1626.9 1646.5L1629.4 1670.4M1604.6 1648.4L1606.3 1672.4M1582.3 1649.6L1583.2 1673.6M1560.0 1634.0L1560.0 1674.0M1537.7 1649.6L1536.8 1673.6M1515.4 1648.4L1513.7 1672.4M1493.1 1646.5L1490.6 1670.4M1470.9 1643.8L1467.6 1667.5M1451.6 1624.5L1444.7 1663.9M1426.9 1636.0L1421.9 1659.5M1405.2 1631.0L1399.4 1654.3M1383.6 1625.2L1377.0 1648.3M1362.2 1618.7L1354.8 1641.5M1346.6 1596.4L1332.9 1634.0M1320.3 1603.4L1311.3 1625.7M1299.7 1594.7L1289.9 1616.6M1279.4 1585.2L1268.9 1606.8M1259.5 1575.1L1248.3 1596.3M1248.0 1550.4L1228.0 1585.0M1220.9 1552.8L1208.1 1573.1M1202.1 1540.6L1188.7 1560.5M1183.8 1527.8L1169.7 1547.2M1166.0 1514.3L1151.2 1533.2M1158.9 1488.0L1133.2 1518.7M1131.8 1485.6L1115.7 1503.4M1115.4 1470.4L1098.7 1487.6M1099.6 1454.6L1082.4 1471.3M1084.4 1438.2L1066.6 1454.3M1082.0 1411.1L1051.3 1436.8M1055.7 1404.0L1036.8 1418.8M1042.2 1386.2L1022.8 1400.3M1029.4 1367.9L1009.5 1381.3M1017.2 1349.1L996.9 1361.9M1019.6 1322.0L985.0 1342.0M994.9 1310.5L973.7 1321.7M984.8 1290.6L963.2 1301.1M975.3 1270.3L953.4 1280.1M966.6 1249.7L944.3 1258.7M973.6 1223.4L936.0 1237.1M951.3 1207.8L928.5 1215.2M944.8 1186.4L921.7 1193.0M939.0 1164.8L915.7 1170.6M934.0 1143.1L910.5 1148.1M945.5 1118.4L906.1 1125.3M926.2 1099.1L902.5 1102.4M923.5 1076.9L899.6 1079.4M921.6 1054.6L897.6 1056.3M920.4 1032.3L896.4 1033.2M936.0 1010.0L896.0 1010.0M920.4 987.7L896.4 986.8M921.6 965.4L897.6 963.7M923.5 943.1L899.6 940.6M926.2 920.9L902.5 917.6M945.5 901.6L906.1 894.7M934.0 876.9L910.5 871.9M939.0 855.2L915.7 849.4M944.8 833.6L921.7 827.0M951.3 812.2L928.5 804.8M973.6 796.6L936.0 782.9M966.6 770.3L944.3 761.3M975.3 749.7L953.4 739.9M984.8 729.4L963.2 718.9M994.9 709.5L973.7 698.3M1019.6 698.0L985.0 678.0M1017.2 670.9L996.9 658.1M1029.4 652.1L1009.5 638.7M1042.2 633.8L1022.8 619.7M1055.7 616.0L1036.8 601.2M1082.0 608.9L1051.3 583.2M1084.4 581.8L1066.6 565.7M1099.6 565.4L1082.4 548.7M1115.4 549.6L1098.7 532.4M1131.8 534.4L1115.7 516.6M1158.9 532.0L1133.2 501.3M1166.0 505.7L1151.2 486.8M1183.8 492.2L1169.7 472.8M1202.1 479.4L1188.7 459.5M1220.9 467.2L1208.1 446.9M1248.0 469.6L1228.0 435.0M1259.5 444.9L1248.3 423.7M1279.4 434.8L1268.9 413.2M1299.7 425.3L1289.9 403.4M1320.3 416.6L1311.3 394.3M1346.6 423.6L1332.9 386.0M1362.2 401.3L1354.8 378.5M1383.6 394.8L1377.0 371.7M1405.2 389.0L1399.4 365.7M1426.9 384.0L1421.9 360.5M1451.6 395.5L1444.7 356.1M1470.9 376.2L1467.6 352.5M1493.1 373.5L1490.6 349.6M1515.4 371.6L1513.7 347.6M1537.7 370.4L1536.8 346.4M1560.0 386.0L1560.0 346.0M1582.3 370.4L1583.2 346.4M1604.6 371.6L1606.3 347.6M1626.9 373.5L1629.4 349.6M1649.1 376.2L1652.4 352.5M1668.4 395.5L1675.3 356.1M1693.1 384.0L1698.1 360.5M1714.8 389.0L1720.6 365.7M1736.4 394.8L1743.0 371.7M1757.8 401.3L1765.2 378.5M1773.4 423.6L1787.1 386.0M1799.7 416.6L1808.7 394.3M1820.3 425.3L1830.1 403.4M1840.6 434.8L1851.1 413.2M1860.5 444.9L1871.7 423.7M1872.0 469.6L1892.0 435.0M1899.1 467.2L1911.9 446.9M1917.9 479.4L1931.3 459.5M1936.2 492.2L1950.3 472.8M1954.0 505.7L1968.8 486.8M1961.1 532.0L1986.8 501.3M1988.2 534.4L2004.3 516.6M2004.6 549.6L2021.3 532.4M2020.4 565.4L2037.6 548.7M2035.6 581.8L2053.4 565.7M2038.0 608.9L2068.7 583.2M2064.3 616.0L2083.2 601.2M2077.8 633.8L2097.2 619.7M2090.6 652.1L2110.5 638.7M2102.8 670.9L2123.1 658.1M2100.4 698.0L2135.0 678.0M2125.1 709.5L2146.3 698.3M2135.2 729.4L2156.8 718.9M2144.7 749.7L2166.6 739.9M2153.4 770.3L2175.7 761.3M2146.4 796.6L2184.0 782.9M2168.7 812.2L2191.5 804.8M2175.2 833.6L2198.3 827.0M2181.0 855.2L2204.3 849.4M2186.0 876.9L2209.5 871.9M2174.5 901.6L2213.9 894.7M2193.8 920.9L2217.5 917.6M2196.5 943.1L2220.4 940.6M2198.4 965.4L2222.4 963.7M2199.6 987.7L2223.6 986.8\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.4\"/><ellipse cx=\"1560\" cy=\"1010\" rx=\"1210\" ry=\"360\" transform=\"rotate(-23.4 1560 1010)\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.5\"/><path d=\"M1560 -40L1560 1480\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.4\"/><path d=\"M-40 1010L2600 1010\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.3\"/><path d=\"M1459 274h14M1466 267v14M327 194h20M337 184v20M515 494h20M525 484v20M370 639h14M377 632v14M286 208h14M293 201v14M1845 191h14M1852 184v14M504 684h14M511 677v14M372 966h20M382 956v20M637 348h20M647 338v20M383 710h20M393 700v20M1757 170h14M1764 163v14\" style=\"stroke:var(--line);fill:none;stroke-width:1.5;opacity:0.75\"/></svg>";
  var GODS = [{"id": "saturnus", "name": "Saturnus", "wall": "../assets/Wallpapers/saturnus.jpg", "plate": "Saturnus with his sickle, lord of time, in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592", "disc": [1320, 610, 250]}, {"id": "janus", "name": "Janus", "wall": "../assets/Wallpapers/janus.jpg", "plate": "Janus with both faces opens the door of the year. Engraved by Robert van Audenaerd after Carlo Maratta", "disc": [1110, 450, 300]}, {"id": "apollo", "name": "Apollo", "wall": "../assets/Wallpapers/apollo.jpg", "plate": "Apollo as Sol, the sun, with lyre and quiver in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592", "disc": [1297, 585, 250]}, {"id": "mars", "name": "Mars", "wall": "../assets/Wallpapers/mars.jpg", "plate": "Mars in armour, a dragon on his helmet. Hubert Quellinus after the statue by Artus Quellinus, Amsterdam, 1655", "disc": [1060, 560, 260]}, {"id": "vulcanus", "name": "Vulcanus", "wall": "../assets/Wallpapers/vulcanus.jpg", "plate": "Vulcanus, the smith of the gods, in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592", "disc": [1320, 560, 250]}, {"id": "neptunus", "name": "Neptunus", "wall": "../assets/Wallpapers/neptunus.jpg", "plate": "Neptunus with his crown and trident, in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592", "disc": [1420, 660, 250]}, {"id": "pluto", "name": "Pluto", "wall": "../assets/Wallpapers/pluto.jpg", "plate": "Pluto in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592", "disc": [1335, 475, 260]}, {"id": "bacchus", "name": "Bacchus", "wall": "../assets/Wallpapers/bacchus.jpg", "plate": "Bacchus in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592", "disc": [1330, 490, 260]}];   // [{id, name, wall, plate}] in the order of the theme picker, the default first
  var BASE = (document.currentScript && document.currentScript.src) || location.href;
  GODS.forEach(function (g) { try { g.wall = new URL(g.wall, BASE).href; } catch (e) {} });
  var K = {};
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  K.icons = Object.keys(ICONS);
  K.icon = function (name) {
    return '<svg viewBox="0 0 24 24" aria-hidden="true">' + (ICONS[name] || '') + '</svg>';
  };
  K.wallpaper = function () { return WALL; };
  K.reduced = function () {
    return document.documentElement.getAttribute('data-motion') === 'reduced' ||
      (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  };
  function each(root, sel, fn) { Array.prototype.forEach.call(root.querySelectorAll(sel), fn); }
  function emit(el, name, detail) { el.dispatchEvent(new CustomEvent(name, { bubbles: true, detail: detail })); }

  /* Segmented: the thumb glides, labels stay where they are */
  K.segmented = function (el) {
    if (el._k) return el._k;
    var buttons = Array.prototype.slice.call(el.querySelectorAll('button'));
    var thumb = document.createElement('i');
    thumb.className = 'k-seg-thumb';
    el.insertBefore(thumb, el.firstChild);
    el.setAttribute('role', 'tablist');
    el.setAttribute('data-ready', '0');
    var index = Math.max(0, buttons.findIndex(function (b) { return b.getAttribute('aria-selected') === 'true'; }));
    function place() {
      var b = buttons[index];
      thumb.style.width = b.offsetWidth + 'px';
      thumb.style.transform = 'translateX(' + b.offsetLeft + 'px)';
    }
    function select(i, silent) {
      var from = index;
      index = Math.max(0, Math.min(buttons.length - 1, i));
      buttons.forEach(function (b, n) {
        b.setAttribute('role', 'tab');
        b.setAttribute('aria-selected', n === index ? 'true' : 'false');
        b.tabIndex = n === index ? 0 : -1;
      });
      place();
      var target = el.getAttribute('data-for');
      if (target) {
        var tabs = document.querySelector(target);
        if (tabs) {
          tabs.style.setProperty('--dir', index >= from ? 1 : -1);
          Array.prototype.forEach.call(tabs.children, function (s, n) {
            if (n === index) s.setAttribute('data-active', ''); else s.removeAttribute('data-active');
          });
        }
      }
      if (!silent) emit(el, 'change', { index: index, value: buttons[index].value || buttons[index].textContent.trim() });
    }
    buttons.forEach(function (b, n) { b.addEventListener('click', function () { select(n); }); });
    el.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        select(index + (e.key === 'ArrowRight' ? 1 : -1));
        buttons[index].focus();
      }
    });
    select(index, true);
    requestAnimationFrame(function () { place(); requestAnimationFrame(function () { el.setAttribute('data-ready', '1'); }); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(place);
    window.addEventListener('resize', place);
    el._k = { select: select, place: place, get index() { return index; } };
    return el._k;
  };

  /* Slider: keeps the filled part and the output in step */
  K.slider = function (input) {
    if (input._k) return; input._k = true;
    function sync() {
      var min = +input.min || 0, max = +input.max || 100;
      input.style.setProperty('--p', ((input.value - min) / (max - min)) * 100 + '%');
      var out = input.parentNode.querySelector('output');
      if (out) out.textContent = input.value + (input.getAttribute('data-unit') || '');
    }
    input.addEventListener('input', sync);
    sync();
  };

  /* Ring gauge */
  K.ring = function (el, value) {
    var r = 28, c = 2 * Math.PI * r;
    if (!el._k) {
      el.insertAdjacentHTML('afterbegin', '<svg viewBox="0 0 60 60"><circle class="t" cx="30" cy="30" r="' + r + '"/><circle class="v" cx="30" cy="30" r="' + r + '" stroke-dasharray="' + c + '" stroke-dashoffset="' + c + '"/></svg>');
      el._k = el.querySelector('.v');
      if (!el.querySelector('b')) el.insertAdjacentHTML('beforeend', '<b><span class="k-roll"></span>%</b>');
    }
    if (value == null) value = +el.getAttribute('data-value') || 0;
    el.setAttribute('data-value', value);
    var v = el._k;
    requestAnimationFrame(function () { v.style.strokeDashoffset = c * (1 - value / 100); });
    var roll = el.querySelector('.k-roll');
    if (roll) K.roll(roll, String(Math.round(value)));
  };

  /* Rolling numbers: every digit is a column that slides */
  K.roll = function (el, text) {
    if (text == null) text = el.getAttribute('data-value') || el.textContent;
    text = String(text);
    if (el._len !== text.length) {
      el.innerHTML = '';
      text.split('').forEach(function (ch) {
        var col = document.createElement('span');
        col.innerHTML = /\d/.test(ch) ? '<i>0</i><i>1</i><i>2</i><i>3</i><i>4</i><i>5</i><i>6</i><i>7</i><i>8</i><i>9</i>' : '<i>' + ch + '</i>';
        el.appendChild(col);
      });
      el._len = text.length;
    }
    Array.prototype.forEach.call(el.children, function (col, n) {
      var ch = text[n];
      if (/\d/.test(ch) && col.children.length === 10) col.style.transform = 'translateY(' + (-1.2 * +ch) + 'em)';
      else if (col.children.length === 1) col.firstChild.textContent = ch;
    });
    el.setAttribute('aria-label', text);
  };

  /* Calendar: one month, Monday first */
  K.calendar = function (el, date) {
    var today = date || (el.getAttribute('data-date') ? new Date(el.getAttribute('data-date')) : new Date());
    var shown = new Date(today.getFullYear(), today.getMonth(), 1);
    function draw() {
      var y = shown.getFullYear(), m = shown.getMonth();
      var first = (new Date(y, m, 1).getDay() + 6) % 7;
      var days = new Date(y, m + 1, 0).getDate(), prev = new Date(y, m, 0).getDate();
      var h = '<header><b>' + MONTHS[m] + ' ' + y + '</b><span><button class="k-iconbtn k-iconbtn-sm" aria-label="Previous month" data-step="-1"><i class="k-icon">' + K.icon('chevron-left') + '</i></button><button class="k-iconbtn k-iconbtn-sm" aria-label="Next month" data-step="1"><i class="k-icon">' + K.icon('chevron-right') + '</i></button></span></header><div class="k-cal-grid">';
      'Mo Tu We Th Fr Sa Su'.split(' ').forEach(function (d) { h += '<span>' + d + '</span>'; });
      for (var i = 0; i < 42; i++) {
        var d = i - first + 1, out = d < 1 || d > days;
        var label = d < 1 ? prev + d : d > days ? d - days : d;
        var cur = !out && d === today.getDate() && m === today.getMonth() && y === today.getFullYear();
        h += '<button' + (out ? ' data-out tabindex="-1"' : '') + (cur ? ' aria-current="date"' : '') + '>' + label + '</button>';
        if (i >= 34 && d >= days) break;
      }
      el.innerHTML = h + '</div>';
      each(el, '[data-step]', function (b) {
        b.addEventListener('click', function () { shown = new Date(y, m + (+b.getAttribute('data-step')), 1); draw(); });
      });
    }
    draw();
  };

  /* Visualizer: bars driven by a level source; without one it idles on a soft synthetic signal */
  K.visualizer = function (el) {
    if (el._k) return el._k;
    var n = +el.getAttribute('data-bars') || 96, bars = [], t = 0, timer = null;
    for (var i = 0; i < n; i++) { var b = document.createElement('i'); el.appendChild(b); bars.push(b); }
    function frame(levels) {
      t += 1;
      bars.forEach(function (b, i) {
        var x = i / (n - 1), bell = Math.exp(-Math.pow((x - 0.5) / 0.26, 2));
        var v = levels ? levels[i] : bell * (0.45 + 0.4 * Math.sin(t * 0.7 + i * 0.9) * Math.sin(t * 0.23 + i * 0.31)) + 0.06 + 0.05 * Math.sin(t * 0.5 + i);
        v = Math.max(0.03, Math.min(1, v));
        b.style.transform = 'scaleY(' + v.toFixed(3) + ')';
        if (v > 0.72) b.setAttribute('data-peak', ''); else b.removeAttribute('data-peak');
      });
    }
    function start() { if (!timer && !K.reduced()) timer = setInterval(function () { if (!document.hidden) frame(); }, 110); }
    function stop() { clearInterval(timer); timer = null; }
    frame();
    if (el.getAttribute('data-paused') == null) start();
    el._k = { frame: frame, start: start, stop: stop };
    return el._k;
  };

  /* Carousel of slanted cards. Geometry mirrors bundle.css: card 96, selected 420, overlap 37, gap 3 */
  K.carousel = function (el) {
    if (el._k) return el._k;
    var track = el.querySelector('.k-carousel-track');
    var cards = Array.prototype.slice.call(track.children);
    if (!cards.length) return null;
    var index = Math.max(0, cards.findIndex(function (c) { return c.getAttribute('aria-selected') === 'true'; }));
    var STEP = 96 - 37 + 3, WIDE = 420, OVER = 37;
    function select(i, silent) {
      index = Math.max(0, Math.min(cards.length - 1, i));
      cards.forEach(function (c, n) { c.setAttribute('aria-selected', n === index ? 'true' : 'false'); c.tabIndex = n === index ? 0 : -1; });
      track.style.transform = 'translate(' + (-(index * STEP - OVER + WIDE / 2)) + 'px, -50%)';
      if (!silent) emit(el, 'change', { index: index, value: cards[index].getAttribute('data-value') });
    }
    cards.forEach(function (c, n) {
      c.addEventListener('click', function (e) {
        if (n === index) emit(el, 'apply', { index: n, value: c.getAttribute('data-value'), x: e.clientX, y: e.clientY });
        else select(n);
      });
    });
    el.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); select(index + 1); cards[index].focus(); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); select(index - 1); cards[index].focus(); }
    });
    el.addEventListener('wheel', function (e) { e.preventDefault(); select(index + (e.deltaY > 0 || e.deltaX > 0 ? 1 : -1)); }, { passive: false });
    select(index, true);
    el._k = { select: select, get index() { return index; } };
    return el._k;
  };

  /* Circular reveal from a point. Resolves when the circle covers the layer */
  K.reveal = function (layer, x, y) {
    var r = layer.getBoundingClientRect();
    layer.style.setProperty('--x', (x - r.left) + 'px');
    layer.style.setProperty('--y', (y - r.top) + 'px');
    layer.removeAttribute('data-on');
    void layer.offsetWidth;
    layer.setAttribute('data-on', '');
    return new Promise(function (resolve) {
      var done = false;
      function end() { if (!done) { done = true; resolve(); } }
      layer.addEventListener('transitionend', end, { once: true });
      setTimeout(end, K.reduced() ? 20 : 900);
    });
  };

  /* Dock: a thin tab on the bottom edge. It rises and widens when the pointer reaches the edge,
     and panels grow out of the button that opened them */
  K.dock = function (el) {
    if (el._k) return el._k;
    var edge = el.querySelector('.k-edge'), inner = el.querySelector('.k-edge-in');
    var zone = el.parentNode && el.parentNode.classList.contains('k-dockbar') ? el.parentNode : el;
    var openBtn = null, timer = null, inside = false, pinned = el.hasAttribute('data-pinned');
    function measure() { el.style.setProperty('--w', Math.ceil(inner.scrollWidth) + 2 + 'px'); }
    function show() { clearTimeout(timer); measure(); el.setAttribute('data-out', ''); }
    function hide() {
      clearTimeout(timer);
      timer = setTimeout(function () {
        if (inside || openBtn || pinned || el.contains(document.activeElement)) return;
        el.removeAttribute('data-out');
      }, 420);
    }
    function close() {
      each(el, '.k-panel[data-open]', function (p) { p.removeAttribute('data-open'); });
      each(edge, '[aria-expanded="true"]', function (b) { b.setAttribute('aria-expanded', 'false'); });
      openBtn = null;
      hide();
    }
    function open(btn) {
      var panel = el.querySelector(btn.getAttribute('data-panel'));
      if (!panel) return;
      var same = openBtn === btn;
      each(el, '.k-panel[data-open]', function (p) { p.removeAttribute('data-open'); });
      each(edge, '[aria-expanded="true"]', function (b) { b.setAttribute('aria-expanded', 'false'); });
      openBtn = null;
      if (same) { hide(); return; }
      show();
      var pr = el.getBoundingClientRect(), br = btn.getBoundingClientRect();
      var w = panel.offsetWidth, center = br.left + br.width / 2 - pr.left - (pr.width / 2 - w / 2);
      panel.style.transformOrigin = Math.max(0, Math.min(w, center)) + 'px 100%';
      panel.setAttribute('data-open', '');
      btn.setAttribute('aria-expanded', 'true');
      openBtn = btn;
      var tab = btn.getAttribute('data-tab'), seg = panel.querySelector('.k-seg');
      if (seg && seg._k) { if (tab != null) seg._k.select(+tab, true); setTimeout(seg._k.place, 0); }
      each(panel, '.k-ring', function (r) { K.ring(r, 0); setTimeout(function () { K.ring(r, +r.getAttribute('data-target') || 0); }, 160); });
      emit(el, 'open', { panel: panel });
    }
    each(edge, 'button[data-panel]', function (b) {
      b.setAttribute('aria-expanded', 'false');
      b.addEventListener('click', function (e) { e.stopPropagation(); open(b); });
    });
    zone.addEventListener('mouseenter', function () { inside = true; show(); });
    zone.addEventListener('mouseleave', function () { inside = false; hide(); });
    edge.addEventListener('click', function () { show(); });
    el.addEventListener('focusin', show);
    el.addEventListener('focusout', hide);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    document.addEventListener('click', function (e) { if (!el.contains(e.target)) close(); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    measure();
    if (pinned) show();
    el._k = { open: open, close: close, show: show, hide: hide };
    return el._k;
  };

  /* Fuzzy match. Every query character must appear in order. Word starts and runs score higher,
     so "tp" finds "Theme picker" and "lscs" finds "Lock screen :: Clock style". Returns null or
     { score, hits } where hits are the matched character positions, for highlighting. */
  K.fuzzy = function (query, text) {
    var q = query.toLowerCase().replace(/\s+/g, ''), t = text.toLowerCase();
    if (!q) return { score: 0, hits: [] };
    var hits = [], score = 0, ti = 0, last = -2;
    for (var qi = 0; qi < q.length; qi++) {
      var c = q[qi], found = -1;
      for (var j = ti; j < t.length; j++) {
        if (t[j] !== c) continue;
        var start = j === 0 || /[\s\-_/.:>]/.test(t[j - 1]);
        if (start || found < 0) { found = j; if (start) break; }
      }
      if (found < 0) return null;
      var atStart = found === 0 || /[\s\-_/.:>]/.test(t[found - 1]);
      score += 10 + (atStart ? 14 : 0) + (found === last + 1 ? 9 : 0) - Math.min(found - ti, 8);
      hits.push(found); last = found; ti = found + 1;
    }
    if (t.indexOf(q) === 0) score += 24;
    else if (t.indexOf(q) > 0) score += 10;
    score -= t.length * 0.15;
    return { score: score, hits: hits };
  };

  /* Wraps the matched characters of text in <b>, escaping the rest */
  K.mark = function (text, hits) {
    var out = '', set = {};
    (hits || []).forEach(function (h) { set[h] = 1; });
    for (var i = 0; i < text.length; i++) {
      var ch = text[i].replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      out += set[i] ? '<b>' + ch + '</b>' : ch;
    }
    return out;
  };

  /* Dismiss with the exit animation, then remove */
  K.dismiss = function (el, cls) {
    el.classList.add(cls || 'k-notif-out');
    var done = false;
    function end() { if (!done) { done = true; if (el.parentNode) el.parentNode.removeChild(el); } }
    el.addEventListener('animationend', end, { once: true });
    setTimeout(end, 500);
  };

  /* The theme the page shows: data-theme on <html> (the design system page sets it), else the default */
  K.gods = GODS;
  K.theme = function () {
    var id = document.documentElement.getAttribute('data-theme');
    return GODS.some(function (g) { return g.id === id; }) ? id : GODS[0].id;
  };
  K.god = function (id) {
    id = id || K.theme();
    for (var i = 0; i < GODS.length; i++) if (GODS[i].id === id) return GODS[i];
    return GODS[0];
  };
  /* Calls fn(id) now and every time the page switches theme */
  K.onTheme = function (fn) {
    fn(K.theme());
    var last = K.theme();
    new MutationObserver(function () { var id = K.theme(); if (id !== last) { last = id; fn(id); } })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  };
  /* Wallpapers that follow the theme: .k-wall[data-follow] and img[data-follow] */
  function follow(root) {
    var walls = [], imgs = [], names = [], plates = [];
    each(root, '.k-wall[data-follow]', function (w) { walls.push(w); });
    each(root, 'img[data-follow]', function (i) { imgs.push(i); });
    each(root, '[data-follow-name]', function (n) { names.push(n); });
    each(root, '[data-follow-plate]', function (n) { plates.push(n); });
    if (!walls.length && !imgs.length && !names.length && !plates.length) return;
    K.onTheme(function (id) {
      var g = K.god(id);
      walls.forEach(function (w) { w.style.backgroundImage = 'url("' + g.wall + '")'; });
      imgs.forEach(function (i) { i.src = g.wall; });
      names.forEach(function (n) { n.textContent = g.name; });
      plates.forEach(function (n) { n.textContent = g.plate; });
    });
  }

  K.hydrate = function (root) {
    root = root || document;
    each(root, '.k-icon[data-icon]', function (i) { if (!i.firstChild) i.innerHTML = K.icon(i.getAttribute('data-icon')); });
    each(root, '.k-wall[data-chart]', function (w) { if (!w.firstChild) w.innerHTML = WALL; });
    each(root, '.k-seg', K.segmented);
    each(root, '.k-slider input', K.slider);
    each(root, '.k-ring[data-value]', function (r) { K.ring(r); });
    each(root, '.k-roll[data-value]', function (r) { K.roll(r); });
    each(root, '.k-cal', function (c) { if (!c.firstChild) K.calendar(c); });
    each(root, '.k-viz', K.visualizer);
    each(root, '.k-carousel', K.carousel);
    each(root, '.k-dock', K.dock);
    if (!root.__kFollow) { root.__kFollow = true; follow(root); }
  };

  window.Kit = K;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { K.hydrate(document); });
  else K.hydrate(document);
})();
