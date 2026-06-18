(function ($) {
	"use strict";
	
	const destinations = [
		{ name: "Canada", duration: "3 Days & 2 Nights" },
		{ name: "India", duration: "5 Days & 4 Nights" },
		{ name: "Thailand", duration: "4 Days & 3 Nights" },
		{ name: "United Kingdom", duration: "2 Days & 1 Night" },
		{ name: "Singapore", duration: "3 Days & 2 Nights" },
		{ name: "Dubai", duration: "4 Days & 3 Nights" },
		{ name: "Australia", duration: "6 Days & 5 Nights" }
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