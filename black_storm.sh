#!/bin/bash

# دالة لعرض العنوان مع تأثيرات خاصة
show_header() {
    clear
    echo -e "\e[40m"  # خلفية سوداء
    echo -e "\e[31m"   # لون أحمر
    echo "==================================================="
    echo -e "\e[1;35m"
    echo "   ██████╗ ██╗      █████╗  ██████╗██╗  ██╗███████╗"
    echo "  ██╔═══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔════╝"
    echo "  ██║   ██║██║     ███████║██║     █████╔╝ ███████╗"
    echo "  ██║   ██║██║     ██╔══██║██║     ██╔═██╗ ╚════██║"
    echo "  ╚██████╔╝███████╗██║  ██║╚██████╗██║  ██╗███████║"
    echo "   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝"
    echo -e "\e[0m"
    echo -e "\e[1;31m         S T O R M   T O O L S\e[0m"
    echo -e "\e[31m===================================================\e[0m"
    echo -e "\e[0m"
}

# دالة لعرض القائمة الرئيسية
show_menu() {
    show_header
    echo -e "\e[1;33mالرجاء اختيار الأداة التي تريد فتحها:\e[0m"
    echo -e "\e[1;36m1. instagram\e[0m"
    echo -e "\e[1;36m2. camira\e[0m"
    echo -e "\e[1;36m3. Collect informatino\e[0m"
    echo -e "\e[1;31m4. خروج\e[0m"
    echo -e "\e[31m===================================================\e[0m"
}

# دالة لمعالجة الاختيار
handle_choice() {
    local choice=$1
    case $choice in
        1)
            echo -e "\e[1;32mتم فتح الاداى (العاصفة السوداء)\e[0m"
            python black_storm.py
            ;;
        2)
            echo -e "\e[1;32mتم فتح الأداة الثانية (إعصار الظلام)\e[0m"
            Cam.sh
            ;;
        3)
            echo -e "\e[1;32mتم فتح الأداة الثالثة (زوبعة الهاكرز)\e[0m"
            Collect_information.py
            ;;
        4)
            echo -e "\e[1;31mجارٍ الخروج من Black Storm...\e[0m"
            sleep 1
            echo -e "\e[1;35mاحذر من العاصفة القادمة!\e[0m"
            exit 0
            ;;
        *)
            echo -e "\e[1;31mاختيار غير صحيح! حاول مرة أخرى.\e[0m"
            ;;
    esac
}

# حلقة البرنامج الرئيسية
while true; do
    show_menu
    read -p "$(echo -e '\e[1;33mاختر رقم الأداة (1-4): \e[0m')" choice
    handle_choice "$choice"
    read -p "$(echo -e '\e[1;34mاضغط Enter للعودة إلى القائمة...\e[0m')"
done
