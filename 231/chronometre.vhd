----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    16:01:17 02/18/2025 
-- Design Name: 
-- Module Name:    chronometre - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity chronometre is
    Port ( P : in  STD_LOGIC;
           S : in  STD_LOGIC;
			  
           CLK : in  STD_LOGIC;
           RST : in  STD_LOGIC;
           Q1 : inout STD_LOGIC_VECTOR(3 downto 0);
			  Q2 : inout STD_LOGIC_VECTOR(2 downto 0);
			  SH : inout STD_LOGIC;
			  
			  IE : inout STD_LOGIC;
			  
			  AN : out STD_LOGIC_VECTOR(3 downto 0) := "1111";
			  C : out STD_LOGIC_VECTOR(6 downto 0);
			  
			  CQ1 : inout STD_LOGIC_VECTOR(6 downto 0);
			  CQ2 : inout STD_LOGIC_VECTOR(6 downto 0);
			  SELC : inout STD_LOGIC := '0');
end chronometre;

architecture Behavioral of chronometre is
	--signal RUN : STD_LOGIC;
	signal DCPT_CLKD : STD_LOGIC_VECTOR(24 downto 0);
	signal CPT_CLKD : STD_LOGIC_VECTOR(24 downto 0);
	
	signal DCPT_CLKD_IE : STD_LOGIC_VECTOR(10 downto 0);
	signal CPT_CLKD_IE : STD_LOGIC_VECTOR(10 downto 0);
	--signal SH : STD_LOGIC;
	signal DQ1 : STD_LOGIC_VECTOR(3 downto 0);
	signal DQ2 : STD_LOGIC_VECTOR(2 downto 0);
	signal RUN : STD_LOGIC;
	
	--signal CQ1 : STD_LOGIC_VECTOR(6 downto 0);
	--signal CQ2 : STD_LOGIC_VECTOR(6 downto 0);
	--signal SELC : STD_LOGIC;
begin

-- Start & Stop (reset synchrone)
process(RST,CLK)
begin
	if rising_edge(CLK) then
		if RST = '1' then RUN <= '0';
		elsif S='1' then RUN <= '1';
		elsif P='1' then RUN <= '0';
		end if;
	end if;
end process;

-- 2²⁰ clock divider
process(CLK,RST)
begin
	DCPT_CLKD <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(CPT_CLKD))+1, 25));
	if rising_edge(CLK) then
		CPT_CLKD <= DCPT_CLKD;
		if RST = '1' then
			CPT_CLKD <= (others => '0');
			SH <= '0';
		elsif CPT_CLKD(24) = '1' then
			SH <= not(SH);
			CPT_CLKD <= (others => '0');
		end if;
	end if;
end process;
-- diviseur pour l'afficheur
process(CLK,RST)
begin
	DCPT_CLKD_IE <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(CPT_CLKD_IE))+1, 11));
	if rising_edge(CLK) then
		CPT_CLKD_IE <= DCPT_CLKD_IE;
		if RST = '1' then
			CPT_CLKD_iE <= (others => '0');
			IE <= '0';
		elsif CPT_CLKD_IE(10) = '1' then
			IE <= not(IE);
			CPT_CLKD_IE <= (others => '0');
		end if;
	end if;
end process;

-- compteur secondes unités et dizaines, reset asynchrone
process(CLK, SH, RST)
begin
	DQ1 <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(Q1))+1, 4));
	DQ2 <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(Q2))+1, 3));
	if RST='1' then
		Q1 <= (others => '0');
		Q2 <= (others => '0');
	elsif rising_edge(SH) and RUN='1' then
		Q1 <= DQ1;
		if Q1="1001" then
			Q1 <= (others => '0');
			Q2 <= DQ2;
		end if;
		if Q2="110" then
			Q2 <= (others => '0');
		end if;
		
	end if;
end process;

-- 2 afficheurs 7 segments multiplixés
AN(0) <= '1';
AN(1) <= '1';
AN(2) <= SELC;
AN(3) <= not SELC;
WITH Q1 SELECT
 CQ1 <=  "1000000" WHEN "0000",
			"1111001" WHEN "0001",
			"0100100" WHEN "0010",
			"0110000" WHEN "0011",
			"0011001" WHEN "0100",
			"0010010" WHEN "0101",
			"0000011" WHEN "0110",
			"1111000" WHEN "0111",
			"0000000" WHEN "1000",
			"0011000" WHEN "1001",
			"1111111" WHEN OTHERS;
WITH Q2 SELECT
 CQ2 <=  "1000000" WHEN "000",
			"1111001" WHEN "001",
			"0100100" WHEN "010",
			"0110000" WHEN "011",
			"0011001" WHEN "100",
			"0010010" WHEN "101",
			"0000011" WHEN "110",
			"1111111" WHEN OTHERS;

process(CLK)
begin
	if rising_edge(IE) then
		SELC <= not SELC;
	end if;
end process;

C <= CQ1 WHEN SELC='1' else CQ2;
end Behavioral;

