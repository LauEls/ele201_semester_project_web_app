<script>
    import chartjs from 'chart.js/auto';
    let chartData;
	import { onMount } from 'svelte';
	let temperatures = $state([]);
	let timestamps = $state([]);
	let smarthouse_mac_addresses = $state([]);
	let selected_temperatures = $state([]);
	let selected_timestamps = $state([]);
	let selectedValue = $state('')
	let device_names = $state([]);
	let device_mac_addresses = $state([]);
	let chartValues = [20, 10, 5, 2, 20, 30, 45];
	let chartLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
	let ctx;
	let chartCanvas;
	let chart;

	onMount(async (promise) => {
		const device_endpoint = 'http://localhost:8000/api/registered-devices/'
		// const device_response = await fetch(device_endpoint)
		// const device_data = await device_response.json()

		const smarthouse_endpoint = 'http://localhost:8000/api/smarthouse/'
		// const smarthouse_response = await fetch(smarthouse_endpoint)
		// const smarthouse_data = await smarthouse_response.json()

		const [device_response, smarthouse_response] = await Promise.all([
            fetch(device_endpoint),
            fetch(smarthouse_endpoint)
        ]);

		if (!device_response.ok || !smarthouse_response.ok) {
            throw new Error("Failed to fetch one or more endpoints");
        }

		const device_data = await device_response.json();
        const smarthouse_data = await smarthouse_response.json();

		device_data.forEach(device => {
			device_names.push(device.device_name)
			device_mac_addresses.push(device.mac_address)
		});

		smarthouse_data.forEach(datapoint => {
			temperatures.push(datapoint.temperature)
			timestamps.push(datapoint.timestamp)
			smarthouse_mac_addresses.push(datapoint.mac_address)
		});



		ctx = chartCanvas.getContext('2d');
		chart = new chartjs(ctx, {
			type: 'line',
			data: {
					labels: chartLabels,
					datasets: [{
							label: 'Temperature',
							backgroundColor: 'rgb(255, 99, 132)',
							borderColor: 'rgb(255, 99, 132)',
							data: chartValues
					}]
			}
		});

	});

	function handleChange(event) {
		selectedValue = event.target.value;
		let mac_address = $state('');
		device_names.forEach((device_name, i) => {
			if (selectedValue == device_name) {
				mac_address = device_mac_addresses[i];
			}
		});
		chart.data.labels.length = 0;
		chart.data.datasets[0].data.length = 0;
		smarthouse_mac_addresses.forEach((smarthouse_mac_address, i) => {
			if (smarthouse_mac_address.toLowerCase() == mac_address.toLowerCase()) {
				chart.data.labels.push(timestamps[i]);
				chart.data.datasets[0].data.push(temperatures[i]);
				selected_temperatures.push(temperatures[i]);
				selected_timestamps.push(timestamps[i]);

			}
		});
		chart.update();
		// ctx = chartCanvas.getContext('2d');
		// var chart = new chartjs(ctx, {
		// 	type: 'line',
		// 	data: {
		// 			labels: selected_timestamps,
		// 			datasets: [{
		// 					label: 'Temperature',
		// 					backgroundColor: 'rgb(255, 99, 132)',
		// 					borderColor: 'rgb(255, 99, 132)',
		// 					data: selected_temperatures
		// 			}]
		// 	}
		// });
	}

</script>

<div class="container">
    <h1>Smart House</h1>

	<h2>Temperature</h2>
	

	<div class="form-floating">
	<select class="form-select" id="floatingSelect" aria-label="Floating label select example" onchange={handleChange}>
		<option selected>Select a device</option>
		{#each device_names as device_name}
			<option>{device_name}</option>
		{/each}
		<!-- <option value="1">One</option>
		<option value="2">Two</option>
		<option value="3">Three</option> -->
	</select>
	<label for="floatingSelect">Device Name</label>
	</div>




    <canvas bind:this={chartCanvas} id="myChart"></canvas>
</div>