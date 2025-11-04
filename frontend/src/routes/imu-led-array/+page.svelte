<script>
    import { onMount } from 'svelte';

    let selectedDeviceName = $state('');
    let selectedMacAddress = $state('');
	let device_names = $state([]);
	let device_mac_addresses = $state([]);

    let timestamps = $state([]);
    let imu_mac_addresses = $state([]);
    let imu_angles = $state([]);
    let current_imu_angle = $state(0.0);


    onMount(async (promise) => {
        getData();

        const eventSource = new EventSource('http://localhost:8000/api/events/'); 
		// Listen for a specific event type (e.g., 'message')
		eventSource.addEventListener('imu-msg', function(event) {
            // 'event.data' will contain the data sent from the Django server
            const data = JSON.parse(event.data);
            console.log('Received message:', data);
			imu_angles.push(data.imu_angle);
			timestamps.push(data.timestamp);
			imu_mac_addresses.push(data.mac_address);
            
            if (data.mac_address.toLowerCase() == selectedMacAddress.toLowerCase()) {
                current_imu_angle = data.imu_angle;
			}
            // messages.update(arr => arr.concat(data));
            // Perform actions based on the received data, e.g., update UI
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
		const solar_tracker_endpoint = 'http://localhost:8000/api/imu-led-array/'

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

		timestamps = [];
		imu_mac_addresses = [];
        imu_angles = [];

		device_data.forEach(device => {
			device_names.push(device.device_name)
			device_mac_addresses.push(device.mac_address)
		});

		solar_tracker_data.forEach(datapoint => {
			imu_angles.push(datapoint.imu_angle)
			timestamps.push(datapoint.timestamp)
			imu_mac_addresses.push(datapoint.mac_address)
		});

	}

    function handleChange(event) {
		selectedDeviceName = event.target.value;
        device_names.forEach((device_name, i) => {
			if (selectedDeviceName == device_name) {
				selectedMacAddress = device_mac_addresses[i];
			}
		});

		current_imu_angle = 0.0
		imu_mac_addresses.forEach((imu_mac_address, i) => {
			if (imu_mac_address.toLowerCase() == selectedMacAddress.toLowerCase()) {
				// chart.data.labels.push(timestamps[i]);
				// temperatureChart.data.datasets[0].data.push({x: timestamps[i], y: temperatures[i]});
				// motionChart.data.datasets[0].data.push({x: timestamps[i], y: motions[i]})
				// chart.data.datasets[0].data.push(temperatures[i]);
				// selected_temperatures.push(temperatures[i]);
				// selected_timestamps.push(timestamps[i]);
				current_imu_angle = imu_angles[i];
			}
		});


	}    
</script>

<div class="container">
    <h1>IMU controlled LED array</h1>
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
    <h2>Current Angle: {current_imu_angle} </h2>
</div>