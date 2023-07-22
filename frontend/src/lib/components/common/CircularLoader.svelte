<script lang="ts">
	import CircularProgress from '@smui/circular-progress';

    type Size = "small" | "medium" | "large";
    export let size: Size = "medium";

    function getStyle() {
        switch (size) {
            case "small":
                return "width: 24px; height: 24px;";
            case "medium":
                return "width: 36px; height: 36px;";
            case "large":
                return "width: 48px; height: 48px;";
        }
    }
</script>

<div class="circular-loader">
    <CircularProgress {...$$restProps} style={getStyle()} indeterminate />
</div>

<style>
    .circular-loader {
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
