<script lang="ts">
	let { children } = $props();
</script>

<svelte:head>
	<!-- <link rel="icon" href={favicon} /> -->
	<!-- <nav class="navbar navbar-expand-lg navbar-light bg-light">
		<a href="/">Home</a>
		<a href="/chronometer">Chronometer</a>
		<a href="/solar-tracker">Solar Tracker</a>
		<a href="/piano">Piano</a>
		<a href="/imu-led-array">IMU controlled LED array</a>
		<a href="/remote-controlled-car">Remote-controlled Car</a>
		<a href="/smarthoust">Smarthouse</a>
		<a href="/candle-temperature">Candle Temperature Measurement</a>
	</nav> -->
	

	<nav class="navbar navbar-expand-lg bg-body-tertiary">
	<div class="container-fluid">
		<a class="navbar-brand" href="/">ELE201</a>
		<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarSupportedContent">
			<ul class="navbar-nav me-auto mb-2 mb-lg-0">
				<li class="nav-item">
					<a class="nav-link active" aria-current="page" href="/">Home</a>
				</li>
				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="/semester-projects" role="button" data-bs-toggle="dropdown" aria-expanded="false">
						Semester Projects
					</a>
					<ul class="dropdown-menu">
						<li><a class="dropdown-item" href="/chronometer">Chronometer</a></li>
						<li><a class="dropdown-item" href="/solar-tracker">Solar Tracker</a></li>
						<li><a class="dropdown-item" href="/piano">Piano</a></li>
						<li><a class="dropdown-item" href="/imu-led-array">IMU controlled LED array</a></li>
						<li><a class="dropdown-item" href="/remote-controlled-car">Remote-controlled Car</a></li>
						<li><a class="dropdown-item" href="/smarthouse">Smarthouse</a></li>
						<li><a class="dropdown-item" href="/candle-temperature">Candle Temperature Measurement</a></li>
					</ul>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="/register-device">Register Device</a>
				</li>
			</ul>
		</div>
	</div>
	</nav>


</svelte:head>

{@render children?.()}
