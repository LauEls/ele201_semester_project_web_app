<script>
    import chartjs from 'chart.js/auto';
	import 'chartjs-adapter-moment';
    // let chartData;
	import { onMount } from 'svelte';
	let temperatures = $state([]);
	let motions = $state([]);
	let timestamps = $state([]);
	let smarthouse_mac_addresses = $state([]);
	// let selected_temperatures = $state([]);
	// let selected_timestamps = $state([]);
	let selectedValue = $state('');
	let device_names = $state([]);
	let device_mac_addresses = $state([]);
	// let temperatureChartValues = [{x: '2025-11-03T10:25:23.388848Z', y: 20}, {x: '2025-11-03T10:26:13.362258Z', y: 25}];
	let temperatureChartValues = [];
	// let chartLabels = [];
	let temperatureCtx;
	let temperatureChartCanvas;
	let temperatureChart;
	let motionChartValues = [];
	let motionCtx;
	let motionChartCanvas;
	let motionChart;




	onMount(async (promise) => {
		

		getData();

		temperatureCtx = temperatureChartCanvas.getContext('2d');
		temperatureChart = new chartjs(temperatureCtx, {
			type: 'line',
			data: {
					// labels: chartLabels,
					datasets: [{
							label: 'Temperature',
							backgroundColor: 'rgb(255, 99, 132)',
							borderColor: 'rgb(255, 99, 132)',
							data: temperatureChartValues
					}]
			},
			options: {
				scales: {
					x: {
						type: 'time',
						time: {
							unit: 'second'
						}
					}
				}
			}

		});

		motionCtx = motionChartCanvas.getContext('2d');
		motionChart = new chartjs(motionCtx, {
			type: 'line',
			data: {
					// labels: chartLabels,
					datasets: [{
							label: 'Motion Detected',
							backgroundColor: 'rgb(255, 99, 132)',
							borderColor: 'rgb(255, 99, 132)',
							data: motionChartValues
					}]
			},
			options: {
				scales: {
					x: {
						type: 'time',
						time: {
							unit: 'second'
						}
					}
				}
			}

		});

	});

	async function  getData() {
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

		device_names = [];
		device_mac_addresses = [];
		temperatures = [];
		timestamps = [];
		smarthouse_mac_addresses = [];
		motions = [];

		device_data.forEach(device => {
			device_names.push(device.device_name)
			device_mac_addresses.push(device.mac_address)
		});

		smarthouse_data.forEach(datapoint => {
			temperatures.push(datapoint.temperature)
			if (datapoint.motion_detected) motions.push(1)
			else motions.push(0)
			// let timestamp = new Date(datapoint.timestamp)
			// timestamps.push(timestamp.getTime())
			timestamps.push(datapoint.timestamp)
			smarthouse_mac_addresses.push(datapoint.mac_address)
		});

	}

	function handleChange(event) {
		selectedValue = event.target.value;
		let mac_address = $state('');
		device_names.forEach((device_name, i) => {
			if (selectedValue == device_name) {
				mac_address = device_mac_addresses[i];
			}
		});
		// chart.data.labels.length = 0;
		temperatureChart.data.datasets[0].data.length = 0;
		motionChart.data.datasets[0].data.length = 0;
		smarthouse_mac_addresses.forEach((smarthouse_mac_address, i) => {
			if (smarthouse_mac_address.toLowerCase() == mac_address.toLowerCase()) {
				// chart.data.labels.push(timestamps[i]);
				temperatureChart.data.datasets[0].data.push({x: timestamps[i], y: temperatures[i]});
				motionChart.data.datasets[0].data.push({x: timestamps[i], y: motions[i]})
				// chart.data.datasets[0].data.push(temperatures[i]);
				// selected_temperatures.push(temperatures[i]);
				// selected_timestamps.push(timestamps[i]);

			}
		});
		temperatureChart.update();
		motionChart.update();
	}

</script>

<div class="container">
	<div class="d-flex justify-content-between align-items-center">
		<h1>Smart House</h1>
		
		<!-- <button type="button" onclick={getData} class="btn btn-primary ml-auto">Refresh</button> -->
	
	</div>
	
	

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
	<h2>Temperature</h2>
    <canvas bind:this={temperatureChartCanvas} id="temperature_chart"></canvas>
	<h2>Motion Detected</h2>
	<canvas bind:this={motionChartCanvas} id="motion_chart"></canvas>
</div>