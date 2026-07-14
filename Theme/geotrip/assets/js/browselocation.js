(function ($) {
	"use strict";
	
	const destinations = [
		{ name: "کانادا", duration: "3 روز و 2 شب" },
		{ name: "هند", duration: "5 روز و 4 شب" },
		{ name: "تایلند", duration: "4 روز و 3 شب" },
		{ name: "اسپانیا", duration: "2 روز و 1 شب" },
		{ name: "فرانسه", duration: "3 روز و 2 شب" },
		{ name: "دبی", duration: "4 روز و 3 شب" },
		{ name: "آلمان", duration: "6 روز و 5 شب" }
	  ];

	  document.querySelectorAll(".flightInput").forEach(input => {
		const container = input.closest(".autocomplete-container");
		const suggestionsBox = container.querySelector(".suggestions");

		const showSuggestions = () => {
		  const query = input.value.toLowerCase();
		  suggestionsBox.innerHTML = "";

		  const filtered = destinations.filter(dest =>
			dest.name.toLowerCase().includes(query)
		  );

		  filtered.forEach(dest => {
			const item = document.createElement("div");
			item.className = "suggestion-item";
			item.innerHTML = `
			  <div class="place-name"><i class="bi bi-geo-alt"></i> ${dest.name}</div>
			  <div class="duration">${dest.duration}</div>
			`;
			item.onclick = () => {
			  input.value = dest.name;
			  suggestionsBox.innerHTML = "";
			};
			suggestionsBox.appendChild(item);
		  });
		};

		input.addEventListener("focus", showSuggestions);
		input.addEventListener("input", showSuggestions);
	  });

	  document.addEventListener("click", e => {
		document.querySelectorAll(".suggestions").forEach(box => {
		  if (!e.target.closest(".autocomplete-container")) {
			box.innerHTML = "";
		  }
		});
	  });
	
	
})(this.jQuery);