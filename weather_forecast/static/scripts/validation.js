'use strict';

const meteorologicalServiceDropdown = document.querySelector(
	'#id_meteorological_service'
);

document.addEventListener('DOMContentLoaded', () => {
	fetch('https://egoronishchuk.pythonanywhere.com/services/weathertime', {
		method: 'POST',
		body: JSON.stringify({
			meteorological_service: meteorologicalServiceDropdown.value,
		}),
	})
		.then((response) => response.json())
		.then((result) => {
			const weatherTimeDropdown =
				document.querySelector('#id_forecast_time');
			weatherTimeDropdown.innerHTML = '';
			for (let weatherTime of result['weather_time']) {
				weatherTimeDropdown.append(new Option(weatherTime));
			}
		});
});

meteorologicalServiceDropdown.addEventListener('change', (event) => {
	fetch('https://egoronishchuk.pythonanywhere.com/services/weathertime', {
		method: 'POST',
		body: JSON.stringify({
			meteorological_service: event.target.value,
		}),
	})
		.then((response) => response.json())
		.then((result) => {
			const weatherTimeDropdown =
				document.querySelector('#id_forecast_time');
			weatherTimeDropdown.innerHTML = '';
			for (let weatherTime of result['weather_time']) {
				weatherTimeDropdown.append(new Option(weatherTime));
			}
		});
});

document
	.querySelector('.needs-validation')
	.addEventListener('submit', (event) => {
		if (!event.target.checkValidity()) {
			event.preventDefault();
			event.stopPropagation();
		}
		event.target.classList.add('was-validated');
	});
