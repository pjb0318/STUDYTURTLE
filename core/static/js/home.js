document.addEventListener("DOMContentLoaded", function () {
    // 스크롤 위치에 따른 이미지와 텍스트 애니메이션 처리
    document.addEventListener("scroll", function () {
        // 현재 스크롤 위치
        const scrollTop = window.scrollY;

        // 대상 요소 선택
        const logo = document.getElementById("scroll-logo");
        const title = document.getElementById("scroll-title");
        const text = document.getElementById("scroll-text");

        // 이미지 스크롤 효과
        if (logo) {
            logo.style.transform = `translateY(${scrollTop * 0.3}px)`;  // 이미지가 스크롤에 따라 움직임
            logo.style.opacity = 1 - scrollTop / 600; // 이미지가 스크롤에 따라 점점 투명해짐
        }

        // 텍스트 스크롤 효과
        if (title) {
            title.style.transform = `translateY(${scrollTop * 0.3}px)`; // 제목이 스크롤에 따라 움직임
            title.style.opacity = 1 - scrollTop / 800; // 제목이 점점 투명해짐
        }
        if (text) {
            text.style.transform = `translateY(${scrollTop * 0.2}px)`;  // 텍스트가 스크롤에 따라 움직임
            text.style.opacity = 1 - scrollTop / 900; // 텍스트가 점점 투명해짐
        }
    });

    // 세션 스토리지 확인
    const hasAnimationPlayed = sessionStorage.getItem("introAnimationPlayed");

    // 모든 애니메이션 대상 요소를 선택
    const animatedElements = document.querySelectorAll(".fade-in");

    // 첫 방문 시 애니메이션 실행
    if (!hasAnimationPlayed) {
        animatedElements.forEach((element, index) => {
            setTimeout(() => {
                element.style.opacity = "1";
                element.style.transform = "translateY(0)";
            }, index * 300); // 각 요소마다 300ms씩 지연
        });

        // 애니메이션 실행 상태 저장
        sessionStorage.setItem("introAnimationPlayed", "true");
    } else {
        // 첫 방문이 아닐 경우 즉시 표시
        animatedElements.forEach((element) => {
            element.style.opacity = "1";
            element.style.transform = "translateY(0)";
        });
    }

    // 스크롤 이벤트로 요소가 화면에 나타날 때 애니메이션 실행 (IntersectionObserver)
    const fadeInElements = document.querySelectorAll(".fade-in");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("fade-in-visible");
                }
            });
        },
        { threshold: 0.1 }
    );

    // 모든 fade-in 요소를 옵저버에 등록
    fadeInElements.forEach((element) => observer.observe(element));
});
