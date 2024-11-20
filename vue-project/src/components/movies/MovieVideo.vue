<template>
    <div>
        <div class="Movie-trailer">
            <iframe 
                width="100%" 
                height="100%" 
                src="https://www.youtube.com/embed/ybhXVSAdIRE?autoplay=1&mute=1&controls=0&rel=0&loop=1&playlist=ybhXVSAdIRE&modestbranding=1&showinfo=0"
                frameborder="0" 
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>
            <div class="overlay">
                <div class="content">
                    <h1 class="movie-title">어벤져스</h1>
                    <p class="movie-desc">마블의 대표작! 최강의 히어로들이 모였다!</p>
                    <p class="release-date">2023.11.27 개봉</p>
                    <div class="controls">
                        <button class="control-btn detail-btn">상세보기</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>

</script>



<style scoped>
.Movie-trailer {
    position: relative;
    width: 100%;
    height: 600px;
    overflow: hidden;
}

.Movie-trailer iframe {
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        to bottom,
        rgba(0,0,0,0.1) 0%,
        rgba(0,0,0,0.3) 50%,
        rgba(0,0,0,0.7) 100%
    );
    z-index: 1;
    display: flex;
    align-items: flex-end;
    padding: 50px;
}

.content {
    color: white;
    max-width: 800px;
}

.movie-title {
    font-size: 3em;
    font-weight: bold;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.movie-desc {
    font-size: 1.2em;
    margin-bottom: 10px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

.release-date {
    font-size: 1em;
    color: #ccc;
    margin-bottom: 20px;
}

.controls {
    display: flex;
    gap: 15px;
    align-items: center;
}

.control-btn {
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.detail-btn {
    background-color: #e71a0f;
    color: white;
    font-weight: bold;
}



.detail-btn:hover {
    background-color: #c41810;
}


</style>

