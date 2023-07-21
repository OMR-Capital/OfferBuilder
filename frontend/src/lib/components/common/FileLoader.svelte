<script lang="ts">
	import Button, { Label } from '@smui/button';

	export let base64Data: string;
	export let allowedExtensions: string[] | null = null;

	let file: File;

	function handleFileInputChange(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input?.files && input.files.length > 0) {
			const selectedFile = input.files[0];
			if (selectedFile && isValidExtension(selectedFile.name)) {
				file = selectedFile;
				readFile();
			} else {
				base64Data = '';
			}
		}
	}

	function isValidExtension(fileName: string) {
		if (!allowedExtensions) {
			return true;
		}
		const extension = fileName.split('.').pop()?.toLowerCase() || '';
		return allowedExtensions.includes(extension);
	}

	function readFile() {
		const reader = new FileReader();
		reader.onloadend = () => {
			if (typeof reader.result === 'string') {
				const base64String = reader.result.split(',')[1]; // Remove the data header
				base64Data = base64String;
			}
		};
		reader.readAsDataURL(file);
	}

	function openFileDialog() {
		const fileInput = document.getElementById('file-input');
		if (fileInput) {
			fileInput.click();
		}
	}

	function shortenFileName(fileName: string) {
		const maxFileNameLength = 25;
		if (fileName.length > maxFileNameLength) {
			return fileName.slice(0, maxFileNameLength) + '...';
		}
		return fileName;
	}
</script>

<div>
	<Button style="width: 100%" variant="outlined" on:click={openFileDialog}>
		<Label>Загрузить файл</Label>
	</Button>
	<div style="width: 100%">
		{#if file}
			<p>{shortenFileName(file.name)}</p>
		{/if}
	</div>
	<input
		id="file-input"
		hidden
		type="file"
		accept={allowedExtensions?.map((ext) => '.' + ext).join(',')}
		on:change={handleFileInputChange}
	/>
</div>
