class Color_Setting:
    color_list = [[ 
                        "#4575b4",  # deep blue
                        "#91bfdb",  # light blue
                        "#e0f3f8",  # pale blue
                        "#a6d96a",  # light green
                        "#1a9850",  # green
                        "#d9ef8b",  # lime yellow
                        "#fee08b",  # beige
                        "#fdae61",  # soft orange
                        "#f46d43",  # coral orange
                        "#d73027"   # muted red
                        ],
                    [
                        # ── 1차: 핵심 6색 (고채도, 가장 큰 토픽에 배정) ──
                        "#3B4CC0",  # deep blue
                        "#E8432A",  # vermillion red
                        "#009E73",  # teal green
                        "#D55E00",  # burnt orange
                        "#7B2D8E",  # purple
                        "#0072B2",  # steel blue
                        
                        # ── 2차: 중간 채도 6색 ──
                        "#CC79A7",  # muted pink
                        "#56B4E9",  # sky blue
                        "#E69F00",  # golden yellow
                        "#44AA99",  # seafoam
                        "#AA4499",  # plum
                        "#999933",  # olive
                        
                        # ── 3차: 채도를 낮춘 6색 ──
                        "#88CCEE",  # light blue
                        "#DDCC77",  # sand
                        "#882255",  # wine
                        "#332288",  # indigo
                        "#117733",  # forest green
                        "#CC6677",  # dusty rose
                        
                        # ── 4차: 더 연한 6색 ──
                        "#6699CC",  # slate blue
                        "#DDA15E",  # warm tan
                        "#BC6C25",  # sienna
                        "#606C38",  # dark olive
                        "#283618",  # deep moss
                        "#ADC178",  # sage
                        
                        # ── 5차: 마지막 6색 (가장 작은 토픽) ──
                        "#A8DADC",  # pale teal
                        "#457B9D",  # french blue
                        "#E76F51",  # terra cotta
                        "#8D99AE",  # cool gray
                        "#B5838D",  # mauve
                        "#6D6875",  # dim purple
                    ],
                    [
                        "#8c510a",  # dark brown
                        "#bf812d",  # brown-gold
                        "#dfc27d",  # sand yellow
                        "#f6e8c3",  # beige
                        "#c7eae5",  # light aqua
                        "#80cdc1",  # teal
                        "#35978f",  # muted teal
                        "#01665e",  # deep green
                        "#003c30",  # near-black green
                        # "#f5f5f5"   # pale gray (neutral base)
                        "#8f8f8f"
                    ]
                    
                    
                    ]
    color_map_str = ["cool", "viridis"]

    pyplot_color_palette = ["slategrey", "royalblue", "dodgerblue",
                            "seagreen", "forestgreen"]
    pyplot_blue_to_red = ["blue", "indigo", "darkmagenta",
                          "mediumvioletred", "crimson", "red"]