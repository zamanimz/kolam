<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	
	let { children } = $props();
	
	let currentPath = $state('');
	
	if (typeof window !== 'undefined') {
		currentPath = window.location.pathname;
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>Pond Logger - Monitor Your Pond Health</title>
</svelte:head>

<nav class="nav">
	<div class="nav-content">
		<h1 style="font-size: 1.5rem; margin: 0; color: var(--primary);">🐟 Pond Logger</h1>
		<ul class="nav-links">
			<li><a href="/" class={currentPath === '/' ? 'active' : ''}>Dashboard</a></li>
			<li><a href="/add" class={currentPath === '/add' ? 'active' : ''}>Add Reading</a></li>
		</ul>
	</div>
</nav>

{@render children()}
