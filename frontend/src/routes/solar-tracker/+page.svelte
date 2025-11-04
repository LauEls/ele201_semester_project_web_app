<script>
    import chartjs from 'chart.js/auto';
    import 'chartjs-adapter-moment';
    import { onMount } from 'svelte';

    let selectedDeviceName = $state('');
    let selectedMacAddress = $state('');
	let device_names = $state([]);
	let device_mac_addresses = $state([]);

    let timestamps = $state([]);
    let solar_tracker_mac_addresses = $state([]);
    let light_intensities = $state([]);
    let servo_angles = $state([]);
    let current_servo_angle = $state(0.0);

    let lightChartValues = [];
    let lightCtx;
	let lightChartCanvas;
	let lightChart;

    onMount(async (promise) => {
        getData();

		lightCtx = lightChartCanvas.getContext('2d');
		lightChart = new chartjs(lightCtx, {
			type: 'line',
			data: {
					// labels: chartLabels,
					datasets: [{
							label: 'Light Intensity',
							backgroundColor: 'rgb(255, 99, 132)',
							borderColor: 'rgb(255, 99, 132)',
							data: lightChartValues
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

        const eventSource = new EventSource('http://localhost:8000/api/events/'); 
		// Listen for a specific event type (e.g., 'message')
		eventSource.addEventListener('solar-tracker-msg', function(event) {
            // 'event.data' will contain the data sent from the Django server
            const data = JSON.parse(event.data);
            console.log('Received message:', data);
            light_intensities.push(data.light_intensity);
			servo_angles.push(data.servo_angle);
			timestamps.push(data.timestamp);
			solar_tracker_mac_addresses.push(data.mac_address);
            
            if (data.mac_address.toLowerCase() == selectedMacAddress.toLowerCase()) {
				lightChart.data.datasets[0].data.push({x: data.timestamp, y: data.light_intensity});
                current_servo_angle = data.servo_angle;

                lightChart.update();
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
		const solar_tracker_endpoint = 'http://localhost:8000/api/solar-tracker/'

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
		solar_tracker_mac_addresses = [];
		light_intensities = [];
        servo_angles = [];

		device_data.forEach(device => {
			device_names.push(device.device_name)
			device_mac_addresses.push(device.mac_address)
		});

		solar_tracker_data.forEach(datapoint => {
			light_intensities.push(datapoint.light_intensity)
			servo_angles.push(datapoint.servo_angle)
			timestamps.push(datapoint.timestamp)
			solar_tracker_mac_addresses.push(datapoint.mac_address)
		});

	}

    function handleChange(event) {
		selectedDeviceName = event.target.value;
        updateChart();
	}

    function updateChart() {
        // let mac_address = $state('');
		device_names.forEach((device_name, i) => {
			if (selectedDeviceName == device_name) {
				selectedMacAddress = device_mac_addresses[i];
			}
		});
		// chart.data.labels.length = 0;
		lightChart.data.datasets[0].data.length = 0;
		solar_tracker_mac_addresses.forEach((solar_tracker_mac_address, i) => {
			if (solar_tracker_mac_address.toLowerCase() == selectedMacAddress.toLowerCase()) {
				lightChart.data.datasets[0].data.push({x: timestamps[i], y: light_intensities[i]});
                current_servo_angle = servo_angles[i];
			}
		});
		lightChart.update();
    }
</script>

<div class="container">
    <h1>Solar Tracker</h1>
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
    <h2>Current Servo Angle: {current_servo_angle}</h2>
    <h2>Light Intensity</h2>
    <canvas bind:this={lightChartCanvas} id="light_chart"></canvas>
</div>