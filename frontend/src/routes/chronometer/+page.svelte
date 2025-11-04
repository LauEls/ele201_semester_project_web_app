<script>
	import { onMount } from 'svelte';

	let selectedDeviceName = $state('');
    let selectedMacAddress = $state('');
	let device_names = $state([]);
	let device_mac_addresses = $state([]);

    let chronometer_mac_addresses = $state([]);
	let messages = $state([]);
	let current_messages = $state([]);

	onMount(async (promise) => {
		getData();

		const eventSource = new EventSource('http://localhost:8000/api/events/'); 
		// Listen for a specific event type (e.g., 'message')
		eventSource.addEventListener('chronometer-msg', function(event) {
			// 'event.data' will contain the data sent from the Django server
			const data = JSON.parse(event.data);
			console.log('Received message:', data);
			messages.push(data.message);
			chronometer_mac_addresses.push(data.mac_address);
		});

		// Listen for the 'open' event, which fires when the connection is established
		eventSource.onopen = function() {
		console.log('SSE connection opened.');
		};

		// Listen for the 'error' event, which fires if the connection encounters an error
		eventSource.onerror = function(error) {
		console.error('SSE error:', error);
		// Handle reconnection or display an error message
		};

		return () => eventSource.close();
	});

	async function  getData() {
		const device_endpoint = 'http://localhost:8000/api/registered-devices/'
		const solar_tracker_endpoint = 'http://localhost:8000/api/chronometer/'

		const [device_response, solar_tracker_response] = await Promise.all([
            fetch(device_endpoint),
            fetch(solar_tracker_endpoint)
        ]);

		if (!device_response.ok || !solar_tracker_response.ok) {
            throw new Error("Failed to fetch one or more endpoints");
        }

		const device_data = await device_response.json();
        const solar_tracker_data = await solar_tracker_response.json();

		device_names = [];
		device_mac_addresses = [];

		chronometer_mac_addresses = [];
		messages = [];

		device_data.forEach(device => {
			device_names.push(device.device_name)
			device_mac_addresses.push(device.mac_address)
		});

		solar_tracker_data.forEach(datapoint => {
			messages.push(datapoint.message)
			chronometer_mac_addresses.push(datapoint.mac_address)
		});

	}

	function handleChange(event) {
		selectedDeviceName = event.target.value;
        device_names.forEach((device_name, i) => {
			if (selectedDeviceName == device_name) {
				selectedMacAddress = device_mac_addresses[i];
			}
		});

		current_messages = [];
		chronometer_mac_addresses.forEach((chronometer_mac_address, i) => {
			if (chronometer_mac_address.toLowerCase() == selectedMacAddress.toLowerCase()) {
				// chart.data.labels.push(timestamps[i]);
				// temperatureChart.data.datasets[0].data.push({x: timestamps[i], y: temperatures[i]});
				// motionChart.data.datasets[0].data.push({x: timestamps[i], y: motions[i]})
				// chart.data.datasets[0].data.push(temperatures[i]);
				// selected_temperatures.push(temperatures[i]);
				// selected_timestamps.push(timestamps[i]);
				current_messages.push(messages[i])
			}
		});
	}

</script>

<div class="container">
    <h1>Chronometer</h1>
	<div class="form-floating">
		<select class="form-select" id="floatingSelect" aria-label="Floating label select example" onchange={handleChange}>
			<option selected>Select a device</option>
			{#each device_names as device_name}
				<option>{device_name}</option>
			{/each}
		</select>
		<label for="floatingSelect">Device Name</label>
	</div>
	
	<h3>Message Output:</h3>
    {#each current_messages as m}
        <p>
            {m}
        </p>
    {/each}
</div>