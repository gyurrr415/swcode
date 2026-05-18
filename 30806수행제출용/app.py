import streamlit as st
from PIL import Image, ImageDraw

from dijkstra import dijkstra
from graph import graph
from data import rooms, positions


# ======================
# 기본 설정
# ======================

st.set_page_config(
    page_title="교내 최단경로 길찾기",
    layout="wide"
)

st.title("교내 최단경로 길찾기 시스템")


# ======================
# 지도 선택 함수
# ======================

def get_map_image(place):

    info = positions[place]

    building = info["building"]
    floor = info["floor"]

    # 실외
    if building == "실외":
        return "maps/campus.png"

    # 층별 지도
    if floor == 1:
        return "maps/floor1.png"

    elif floor == 2:
        return "maps/floor2.png"

    elif floor == 3:
        return "maps/floor3.png"

    elif floor == 4:
        return "maps/floor4.png"


# ======================
# 선 + 점 그리기 함수
# ======================

def draw_path(image_path, points, title):

    image = Image.open(image_path)

    draw = ImageDraw.Draw(image)

    # 선
    for i in range(len(points) - 1):

        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        draw.line(
            (x1, y1, x2, y2),
            fill="blue",
            width=6
        )

    # 점
    for i, (x, y) in enumerate(points):

        color = "yellow"

        if i == 0:
            color = "green"

        elif i == len(points) - 1:
            color = "red"

        draw.ellipse(
            (x - 12, y - 12, x + 12, y + 12),
            fill=color
        )

    st.image(
        image,
        caption=title,
        use_container_width=True
    )


# ======================
# 화면 분할
# ======================

col1, col2 = st.columns([2, 1])


# ======================
# 길찾기
# ======================

with col1:

    st.header("길찾기")

    start = st.selectbox(
        "출발지 선택",
        rooms
    )

    end = st.selectbox(
        "도착지 선택",
        rooms
    )

    if st.button("길찾기 시작"):

        cost, path = dijkstra(
            graph,
            start,
            end
        )

        if cost == float("inf"):

            st.error("경로를 찾을 수 없습니다.")

        else:

            st.success(f"최단 거리 비용: {cost}")

            st.write(" → ".join(path))

            start_info = positions[start]
            end_info = positions[end]

            start_building = start_info["building"]
            end_building = end_info["building"]

            start_floor = start_info["floor"]
            end_floor = end_info["floor"]

            # ======================
            # 같은 층
            # ======================

            if (
                start_building == end_building
                and
                start_floor == end_floor
            ):

                image_path = get_map_image(start)

                points = [

                    (
                        start_info["x"],
                        start_info["y"]
                    ),

                    (
                        end_info["x"],
                        end_info["y"]
                    )

                ]

                draw_path(
                    image_path,
                    points,
                    f"{start_floor}층 이동 경로"
                )

            # ======================
            # 같은 건물 다른 층
            # ======================

            elif (
                start_building == end_building
                and
                start_building != "실외"
            ):

                start_stair = f"{start_building}{start_floor}층계단"

                end_stair = f"{end_building}{end_floor}층계단"

                # 출발층
                start_image = get_map_image(start)

                start_points = [

                    (
                        start_info["x"],
                        start_info["y"]
                    ),

                    (
                        positions[start_stair]["x"],
                        positions[start_stair]["y"]
                    )

                ]

                draw_path(
                    start_image,
                    start_points,
                    f"{start_floor}층 → 계단"
                )

                # 도착층
                end_image = get_map_image(end)

                end_points = [

                    (
                        positions[end_stair]["x"],
                        positions[end_stair]["y"]
                    ),

                    (
                        end_info["x"],
                        end_info["y"]
                    )

                ]

                draw_path(
                    end_image,
                    end_points,
                    f"계단 → {end_floor}층"
                )

            # ======================
            # 건물 이동 / 실외 이동
            # ======================

            else:

                building_entrance = {
                    "본관": "본관입구",
                    "후관": "후관입구",
                    "별관": "별관입구",
                    "실외": None
                }

                start_entrance = building_entrance.get(start_building)

                end_entrance = building_entrance.get(end_building)

                # ======================
                # 출발 건물
                # ======================

                if start_building != "실외":

                    start_image = get_map_image(start)

                    start_points = [

                        (
                            start_info["x"],
                            start_info["y"]
                        ),

                        (
                            positions[start_entrance]["x"],
                            positions[start_entrance]["y"]
                        )

                    ]

                    draw_path(
                        start_image,
                        start_points,
                        "출발 건물 이동"
                    )

                # ======================
                # 실외 이동
                # ======================

                outdoor_points = []

                # 출발
                if start_building == "실외":

                    outdoor_points.append(
                        (
                            start_info["x"],
                            start_info["y"]
                        )
                    )

                else:

                    outdoor_points.append(
                        (
                            positions[start_entrance]["x"],
                            positions[start_entrance]["y"]
                        )
                    )

                # 도착
                if end_building == "실외":

                    outdoor_points.append(
                        (
                            end_info["x"],
                            end_info["y"]
                        )
                    )

                else:

                    outdoor_points.append(
                        (
                            positions[end_entrance]["x"],
                            positions[end_entrance]["y"]
                        )
                    )

                draw_path(
                    "maps/campus.png",
                    outdoor_points,
                    "실외 이동"
                )

                # ======================
                # 도착 건물
                # ======================

                if end_building != "실외":

                    end_image = get_map_image(end)

                    end_points = [

                        (
                            positions[end_entrance]["x"],
                            positions[end_entrance]["y"]
                        ),

                        (
                            end_info["x"],
                            end_info["y"]
                        )

                    ]

                    draw_path(
                        end_image,
                        end_points,
                        "도착 건물 이동"
                    )


# ======================
# 게시판
# ======================

with col2:

    st.header("오류 제보 게시판")

    post = st.text_area(
        "오류 / 건의사항 작성"
    )

    if st.button("게시글 등록"):

        if post.strip() != "":

            with open(
                "posts/posts.txt",
                "a",
                encoding="utf-8"
            ) as f:

                f.write(post + "\n")

            st.success("등록 완료")

    st.divider()

    st.subheader("게시글 목록")

    try:

        with open(
            "posts/posts.txt",
            "r",
            encoding="utf-8"
        ) as f:

            posts = f.readlines()

        if len(posts) == 0:

            st.info("게시글 없음")

        else:

            for p in posts[::-1]:

                st.info(p)

    except:

        st.info("게시글 없음")